"""
cd2t main classes
"""
import copy
from cd2t.errors import SchemaError
from cd2t.references import ReferenceFinding
from cd2t.results import FindingsList
from cd2t.run_time_env import RunTimeEnv
import cd2t.schema
import cd2t.types.parser


class DataParser:
    """Mother class for all data processing classes"""

    def __init__(self, namespace: str = "") -> None:
        # pylint: disable-next=invalid-name
        self.RTE = RunTimeEnv(namespace=namespace)
        self.current_schema = None

    @property
    def namespace(self):
        return self.RTE.namespace

    def change_namespace(self, namespace: str) -> None:
        self.RTE.change_namespace(namespace=namespace)

    def _get_schema(self, schema: cd2t.schema.Schema) -> cd2t.schema.Schema:
        """Return a schema object. Either given schema if valid or last loaded schema

        Args:
            schema: Schema object

        Return:
            A valid Schema object

        Raises:
            SchemaError:
                - If given schema is not a Schema object
                - If given schema object is not valid and no schema has been loaded before
        """
        if not isinstance(schema, cd2t.schema.Schema):
            raise SchemaError("Given schema is not a valid schema object")
        if schema.root_data_type is None:
            if self.current_schema is None:
                raise SchemaError(
                    "need a schema or " + "Validator object loads a schema first"
                )
            return self.current_schema
        return schema

    def load_schema(self, schema_definition: dict) -> cd2t.schema.Schema:
        """Verify schema definition, converts it to a Schema object and stores it.

        Args:
            schema_definition: dictionary - containing schema definition

        Return:
            A valid Schema object

        Raises:
            SchemaError: If given schema definition is not a dictionary
                         or not a valid schema definition
        """
        # pylint: disable=too-many-branches
        schema_definition = copy.deepcopy(schema_definition)

        version = schema_definition.get("version", 1)
        if not isinstance(version, int):
            raise SchemaError("Schema version must be 'integer'")
        if version not in [1, 2]:
            raise SchemaError(f"Schema version {version} not support.")
        schema = cd2t.schema.Schema(
            version=version,
            description=schema_definition.get("description", ""),
            allow_shortcuts=schema_definition.get(
                "allow_data_type_shortcuts", version > 1
            ),
        )

        if schema.version == 2:
            if "subschemas" in schema_definition.keys():
                raise SchemaError("Subschemas not supported in version 2")
            self.RTE.templates = schema_definition.get("templates", {})
            template_merge_options = schema_definition.get("template_merge_options", {})
            self.RTE.templates_merge_recursive = template_merge_options.get(
                "recursive", True
            )
            self.RTE.templates_list_merge = template_merge_options.get(
                "list_merge", "append_rp"
            )
            # Validate, build and store custom data types
            for cdt_name, cdt_schema in schema_definition.get(
                "custom_data_types", {}
            ).items():
                _path = "custom_data_types." + cdt_name
                if not isinstance(cdt_schema, dict):
                    raise SchemaError(
                        message="Custom data type definition must be a dictionary",
                        path=_path,
                    )
                data_type = cd2t.types.parser.ParserDataType().build_schema(
                    schema_definition=cdt_schema,
                    path=_path,
                    RTE=self.RTE,
                    schema=schema,
                )
                if data_type.customizable:
                    if (
                        cdt_name
                        not in cd2t.types.parser.BUILTIN_DATA_TYPES[schema.version]
                    ):
                        schema.custom_data_types[cdt_name] = cdt_schema
                    else:
                        raise SchemaError(
                            message="Custom data type name is a built-in data type name",
                            path=_path,
                        )
                else:
                    raise SchemaError(
                        message=f"Data type {cdt_schema['type']} is not customizable",
                        path=_path,
                    )

        elif schema.version == 1:
            self.RTE.subschemas = schema_definition.get("subschemas", {})
            if self.RTE.subschemas:
                if not isinstance(self.RTE.subschemas, dict):
                    raise SchemaError("Schema subschemas is no dictionary")
                for sub_name, sub_schema in self.RTE.subschemas.items():
                    _path = "<" + sub_name + ">"
                    if isinstance(sub_schema, cd2t.schema.Schema):
                        # This subschema was already verified/translated (recursively)
                        continue
                    sub_type_schema = sub_schema.get("root", None)
                    if sub_type_schema is None:
                        raise SchemaError(message="key 'root' missing", path=_path)
                    _path = _path + "root"
                    self.RTE.subschema_path.append(sub_name)
                    cd2t.types.parser.ParserDataType().build_schema(
                        schema_definition=sub_type_schema,
                        path=_path,
                        RTE=self.RTE,
                        schema=schema,
                    )
                    self.RTE.subschema_path.pop()

        root_type_schema = schema_definition.get("root", None)
        if root_type_schema is None:
            raise SchemaError(message="key 'root' missing")
        _path = "root"
        root_type = cd2t.types.parser.ParserDataType().build_schema(
            schema_definition=root_type_schema,
            path=_path,
            RTE=self.RTE,
            schema=schema,
        )
        schema.set_root_data_type(root_type)
        self.current_schema = schema

        # Clean RTE
        self.RTE.templates = {}
        self.RTE.subschemas = {}
        return schema

    def get_reference_findings(self) -> list[ReferenceFinding]:
        """Get references findings after data validation(s)

        Returns:
            list - containing all findings as ReferenceFinding objects
        """
        return self.RTE.references.get_producer_consumer_issues()


class Autogenerator(DataParser):
    """
    Autogenerator can:
    - load/verify schema definitions
    - build references on multiple data sets
    - autogenerate data in data sets according to schema definition(s) and references
    """

    def build_references(self, data: any, schema=cd2t.schema.Schema()) -> None:
        """Build/Populate references from data with schema definitions

        Args:
            data: any - Any data from which references should be analyzed

            schema: Schema object
                If not given or Schema object is not valid, last loaded schema is used
        """
        schema = self._get_schema(schema)
        root_data_type = schema.root_data_type
        root_data_type.build_references(data=data, path="", RTE=self.RTE)

    def autogenerate_data(self, data: any, schema=cd2t.schema.Schema()) -> any:
        """Autogenerate missing data according to schema and references

        Args:
            data: any - Any data where missing data should be added

            schema: Schema object
                If not given or Schema object is not valid, last loaded schema is used

        Returns:
            tuple:
                - any - Given 'data' with autogerenated data added
                - FindingsList object - containing all findings as Finding objects
        """
        schema = self._get_schema(schema)
        self.RTE.allow_shortcuts = schema.version > 1
        root_data_type = schema.root_data_type
        new_data, findings = root_data_type.autogenerate_data(
            data=data, path="", RTE=self.RTE
        )
        findings.set_namespace(self.RTE.namespace)
        return new_data, findings


class Validator(DataParser):
    """
    Validator can:
    - load/verify schema definitions
    - validate data according to schema definition(s) and analyzed references
    """

    def validate_data(self, data: any, schema=cd2t.schema.Schema()) -> FindingsList:
        """Validate data according to schema and references

        Args:
            data: any - Any data which should be validated

            schema: Schema object
                If not given or Schema object is not valid, last loaded schema is used

        Returns:
            FindingsList object - containing all findings as Finding objects
        """
        schema = self._get_schema(schema)
        root_data_type = schema.root_data_type
        findings = root_data_type.validate_data(data=data, path="", RTE=self.RTE)
        findings.set_namespace(self.RTE.namespace)
        return findings
