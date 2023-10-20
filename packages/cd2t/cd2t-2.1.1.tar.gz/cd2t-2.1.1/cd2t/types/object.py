"""
Object Data Type Classes
"""
# pylint: disable=invalid-name
import re
from cd2t.errors import SchemaError
from cd2t.results import ValidationFinding, FindingsList
from cd2t.run_time_env import RunTimeEnv
import cd2t.schema
import cd2t.types.base
import cd2t.types.parser
from cd2t.utils import string_matches_regex_list, regex_matches_in_string_list


class Object(cd2t.types.base.BaseDataType):
    # pylint: disable=too-many-instance-attributes
    data_type_name = "object"
    matching_classes = [dict]
    support_reference = True
    options = [
        # option_name, required, class, init_value
        ("attributes", False, dict, None),
        ("required_attributes", False, list, list),
        ("dependencies", False, dict, {}),
        ("reference_attributes", False, list, []),
        ("ignore_undefined_attributes", False, bool, False),
        ("allow_regex_attributes", False, bool, False),
        ("autogenerate", False, bool, True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.attributes = None
        self.attributes_objects = {}
        self.tmp_a_schema = None
        self.required_attributes = []
        self.required_xor_attributes = []
        self.dependencies = {}
        self.reference_attributes = []
        self.ignore_undefined_attributes = False
        self.allow_regex_attributes = False
        self.autogenerate = True

    def build_schema(
        self,
        schema_definition: dict,
        path: str,
        RTE: RunTimeEnv,
        schema: cd2t.schema.Schema,
    ):
        super().build_schema(
            schema_definition=schema_definition,
            path=path,
            RTE=RTE,
            schema=schema,
        )
        if self.attributes is not None:
            for a_name, a_schema in self.attributes.items():
                attr_path = f"{path}.{a_name}"
                self.tmp_a_schema = a_schema
                self.attributes_objects[
                    a_name
                ] = cd2t.types.parser.ParserDataType().build_schema(
                    self.tmp_a_schema, attr_path, RTE, schema
                )
        return self

    def verify_options(self, path: str) -> None:
        # pylint: disable=too-many-branches
        super().verify_options(path)
        if self.attributes is None:
            # No other options should be set:
            # pylint: disable-next=unused-variable
            for option, init_value in [(o[0], o[3]) for o in self.options]:
                # pylint: disable-next=exec-used
                if exec("self." + option + " != init_value"):
                    raise SchemaError("Option 'attributes' required", path + option)
            return
        i = 0
        for xor_list in self.required_xor_attributes:
            if not isinstance(xor_list, list):
                raise SchemaError(
                    "Value is not a list",
                    f"{path}required_xor_attributes[{i}]",
                )
            k = 0
            for attr in xor_list:
                if not self._attribute_in_list(
                    attr, list(self.attributes.keys()), self.allow_regex_attributes
                ):
                    raise SchemaError(
                        f"'{attr}' not in 'attributes'",
                        f"{path}required_xor_attributes[{i}][{k}]",
                    )
                k += 1
            i += 1
        for req_attr in self.required_attributes:
            if not self._attribute_in_list(
                req_attr, list(self.attributes.keys()), self.allow_regex_attributes
            ):
                raise SchemaError(
                    f"'{req_attr}' not in 'attributes'",
                    f"{path}required_attributes[{i}]",
                )
            i += 1
        for i, ref_attr in enumerate(self.reference_attributes):
            if ref_attr not in self.attributes.keys():
                raise SchemaError(
                    f"'{ref_attr}' not in 'attributes'",
                    f"{path}reference_attributes[{i}]",
                )
        path = path + "dependencies."
        for dep_attr, dep_info in self.dependencies.items():
            attr_path = path + dep_attr
            if dep_attr not in self.attributes.keys():
                raise SchemaError(f"'{dep_attr}' not in 'attributes'", attr_path)
            if not isinstance(dep_info, dict):
                raise SchemaError("Not a dictionary", attr_path)
            i = 0
            for req_attr in dep_info.get("requires", []):
                if not self._attribute_in_list(
                    req_attr, list(self.attributes.keys()), self.allow_regex_attributes
                ):
                    raise SchemaError(
                        f"'{req_attr}' not in 'attributes'",
                        f"{attr_path}.requires[{i}]",
                    )
                i += 1
            i = 0
            for ex_attr in dep_info.get("excludes", []):
                if not self._attribute_in_list(
                    ex_attr, list(self.attributes.keys()), self.allow_regex_attributes
                ):
                    raise SchemaError(
                        f"'{ex_attr}' not in 'attributes'",
                        f"{attr_path}.excludes[{i}]",
                    )
                i += 1

    def build_references(self, data: any, path: str, RTE: RunTimeEnv):
        for a_name, a_data in data.items():
            data_type = self._get_attribute_object(a_name, self.allow_regex_attributes)
            if data_type is None:
                continue
            attr_path = f"{path}.{a_name}"
            data_type.build_references(a_data, attr_path, RTE)

    def autogenerate_data(self, data: any, path: str, RTE: RunTimeEnv):
        # pylint: disable=too-many-branches
        findings = FindingsList()
        if data is None or not self.data_matches_type(data):
            return data, findings
        if path:
            path = path + "."
        if not self.allow_regex_attributes and self.autogenerate:
            if RTE.ruamel_yaml_available and isinstance(data, RTE.ruamel_commented_map):
                new_data = data
                insert = True
            else:
                new_data = {}
                insert = False
            i = 0
            for a_name, data_type in self.attributes_objects.items():
                attr_path = path + str(a_name)
                _findings = FindingsList()
                if a_name not in data.keys():
                    _data, _findings = data_type.autogenerate_data(
                        data=None, path=attr_path, RTE=RTE
                    )
                    if _findings:
                        if insert:
                            new_data.insert(
                                pos=i, key=a_name, value=_data, comment="autogenerated"
                            )
                        else:
                            new_data[a_name] = _data
                        i += 1
                else:
                    _data, _findings = data_type.autogenerate_data(
                        data[a_name], attr_path, RTE
                    )
                    new_data[a_name] = _data
                    i += 1
                findings += _findings
            data = new_data
        else:
            for a_name, a_data in data.items():
                data_type = self._get_attribute_object(
                    a_name, self.allow_regex_attributes
                )
                if data_type is None:
                    continue
                attr_path = path + str(a_name)
                _data, _findings = data_type.autogenerate_data(a_data, attr_path, RTE)
                if _findings:
                    data[a_name] = _data
                    findings += _findings
        return data, findings

    @staticmethod
    def _attribute_in_list(
        attribute: str, attributes: list, regex_allowed=False
    ) -> bool:
        if regex_allowed:
            return regex_matches_in_string_list(attribute, attributes)
        if attribute in attributes:
            return attribute
        return None

    def _get_attribute_object(self, name: str, regex_allowed=False) -> bool:
        if regex_allowed:
            name = string_matches_regex_list(
                string=name,
                regex_list=list(self.attributes_objects.keys()),
                full_match=True,
            )
        return self.attributes_objects.get(name, None)

    def verify_data(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        findings = FindingsList()
        if self.attributes is None:
            return findings
        path_dot = path + "." if path else ""
        # Find not allowed attributes
        for a_name, a_data in data.items():
            attr_path = path_dot + str(a_name)
            data_type = self._get_attribute_object(a_name, self.allow_regex_attributes)
            if data_type is None:
                if self.ignore_undefined_attributes:
                    continue
                findings.append(
                    ValidationFinding(path=attr_path, message="Attribute not allowed")
                )
                continue
            findings += data_type.validate_data(data=a_data, path=attr_path, RTE=RTE)
        # Validate xor attributes
        for xor_list in self.required_xor_attributes:
            found = 0 if xor_list else 1
            attributes_found = []
            for attr in data:
                if self.allow_regex_attributes:
                    for req_attr_regex in xor_list:
                        if re.match(req_attr_regex, attr):
                            found += 1
                            attributes_found.append(str(attr))
                elif attr in xor_list:
                    found += 1
                    attributes_found.append(str(attr))
            if found == 0:
                message = "One of these attributes must be set: "
                for attr in xor_list:
                    message += f", {str(attr)}"
                findings.append(ValidationFinding(path=path, message=message))
            elif found > 1:
                findings.append(
                    ValidationFinding(
                        path=path,
                        message="Only one of these attributes are allowed: "
                        + ", ".join(attributes_found),
                    )
                )
        # Validate required attributes
        for req_attr in self.required_attributes:
            attr_path = path_dot + str(req_attr)
            found_in_data_keys = False
            if self.allow_regex_attributes:
                if regex_matches_in_string_list(
                    regex=req_attr, strings=list(data.keys()), full_match=True
                ):
                    found_in_data_keys = True
            elif req_attr in data.keys():
                found_in_data_keys = True
            if not found_in_data_keys:
                findings.append(
                    ValidationFinding(
                        path=attr_path, message="Required attribute missing"
                    )
                )
        for attr_name, dep_info in self.dependencies.items():
            if not attr_name in data.keys():
                continue
            attr_path = path_dot + str(attr_name)
            for req_attr in dep_info.get("requires", []):
                if self.allow_regex_attributes:
                    if not regex_matches_in_string_list(
                        regex=req_attr, strings=list(data.keys()), full_match=True
                    ):
                        findings.append(
                            ValidationFinding(
                                path=attr_path,
                                message="No attribute matches regex requirements",
                            )
                        )
                elif req_attr not in data.keys():
                    findings.append(
                        ValidationFinding(
                            path=attr_path, message=f"Missing attribute '{req_attr}'"
                        )
                    )
            for ex_attr in dep_info.get("excludes", []):
                match = None
                if self.allow_regex_attributes:
                    match = regex_matches_in_string_list(
                        regex=ex_attr, strings=list(data.keys()), full_match=True
                    )
                    if match:
                        found_in_data_keys = True
                elif ex_attr in data.keys():
                    match = ex_attr
                if match is not None:
                    findings.append(
                        ValidationFinding(
                            path=attr_path, message=f"Excludes attribute '{match}'"
                        )
                    )
        return findings

    def get_reference_data(self, data: any, path: str) -> any:
        ref_data = []
        results = []
        for ref_attr in self.reference_attributes:
            if ref_attr not in data.keys():
                results.append(
                    ValidationFinding(
                        path=path, message=f"Reference attribute '{ref_attr}' missing"
                    )
                )
            ref_data.append(data[ref_attr])
        return ref_data, results


class Object_V1(Object):
    def verify_options(self, path: str) -> None:
        super().verify_options(path)
        if not self.reference_attributes:
            if self.ref_key and self.allow_regex_attributes:
                raise SchemaError(
                    "Must be defined if reference is enabled and regex is allowed",
                    path + "reference_attributes",
                )
            self.reference_attributes = self.attributes


class Object_V2(Object):
    options = [
        # option_name, required, class, init_value
        ("attributes", False, dict, None),
        ("required_attributes", False, list, list),
        ("required_xor_attributes", False, list, []),
        ("dependencies", False, dict, {}),
        ("ignore_undefined_attributes", False, bool, False),
        ("allow_regex_attributes", False, bool, False),
        ("autogenerate", False, bool, True),
    ]

    def build_schema(
        self,
        schema_definition: dict,
        path: str,
        RTE: RunTimeEnv,
        schema: cd2t.schema.Schema,
    ):
        # Pop reference.attributes if available
        if (
            isinstance(schema_definition, dict)
            and isinstance(schema_definition.get("reference", None), dict)
            and "attributes" in schema_definition["reference"]
        ):
            self.reference_attributes = schema_definition["reference"].pop("attributes")
        super().build_schema(
            schema_definition=schema_definition,
            path=path,
            RTE=RTE,
            schema=schema,
        )
        return self

    def get_reference_data(self, data: any, path: str) -> any:
        if not self.reference_attributes:
            return data, []

        ref_data = []
        results = []
        if self.reference_attributes:
            for ref_attr in self.reference_attributes:
                if ref_attr not in data.keys():
                    results.append(
                        ValidationFinding(
                            path=path,
                            message=f"Reference attribute '{ref_attr}' missing",
                        )
                    )
                ref_data.append(data[ref_attr])
        return ref_data, results
