"""
IDList Data Type Class
"""
# pylint: disable=invalid-name
from cd2t.errors import SchemaError
from cd2t.references import ReferenceElement, OPT
from cd2t.results import WrongValueFinding, UniqueErrorFinding, FindingsList
from cd2t.run_time_env import RunTimeEnv
import cd2t.schema
import cd2t.types.base
import cd2t.types.datatype
import cd2t.types.integer
import cd2t.types.parser
import cd2t.types.string


class IDList(cd2t.types.base.BaseDataType):
    data_type_name = "idlist"
    matching_classes = [dict]
    support_reference = True
    options = [
        # option_name, required, class
        ("minimum", False, int, None),
        ("maximum", False, int, None),
        ("elements", True, [dict, str], None),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.minimum = None
        self.maximum = None
        self.elements = None
        self.element_type = None
        self.id_data_type = cd2t.types.string.String()

    def build_schema(
        self,
        schema_definition: dict,
        path: str,
        RTE: RunTimeEnv,
        schema: cd2t.schema.Schema,
    ) -> cd2t.types.base.DataType:
        super().build_schema(
            schema_definition=schema_definition,
            path=path,
            RTE=RTE,
            schema=schema,
        )

        self.element_type = cd2t.types.parser.ParserDataType().build_schema(
            schema_definition=self.elements,
            path=path + ".elements",
            RTE=RTE,
            schema=schema,
        )
        return self

    def build_sub_references(self, data: any, path: str, RTE: RunTimeEnv):
        i = 0
        for element in data.values():
            self.element_type.build_references(
                data=element, path=f"{path}[{i}]", RTE=RTE
            )
            i += 1

    def autogenerate_data(self, data: any, path: str, RTE: RunTimeEnv):
        findings = FindingsList()
        if not self.data_matches_type(data):
            return data, findings
        if path:
            path = path + "."
        for _id, element in data.items():
            new_path = path + str(_id)
            _data, _findings = self.element_type.autogenerate_data(
                data=element, path=new_path, RTE=RTE
            )
            data[_id] = _data
            findings += _findings
        return data, findings


class IDList_V1(IDList):
    V1_options = [
        # option_name, required, class
        ("id_type", False, str, "string"),
        ("id_minimum", False, int, None),
        ("id_maximum", False, int, None),
        ("allowed_ids", False, list, None),
        ("not_allowed_ids", False, list, []),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.options.extend(self.V1_options)
        self.id_type = "string"
        self.id_minimum = None
        self.id_maximum = None
        self.allowed_ids = None
        self.not_allowed_ids = []

    def build_schema(
        self,
        schema_definition: dict,
        path: str,
        RTE: RunTimeEnv,
        schema: cd2t.schema.Schema,
    ) -> cd2t.types.base.DataType:
        super().build_schema(
            schema_definition=schema_definition,
            path=path,
            RTE=RTE,
            schema=schema,
        )
        id_type_schema = {}
        if self.id_minimum:
            id_type_schema["minimum"] = self.id_minimum
        if self.id_maximum:
            id_type_schema["maximum"] = self.id_maximum
        if self.not_allowed_ids:
            id_type_schema["not_allowed_values"] = self.not_allowed_ids
        if self.id_type == "string":
            if self.allowed_ids:
                id_type_schema["allowed_values"] = self.allowed_ids
            id_type_schema["regex_mode"] = True
        self.id_data_type = self.id_data_type.build_schema(
            schema_definition=id_type_schema,
            path=path,
            RTE=RTE,
            schema=schema,
        )
        return self

    def verify_options(self, path: str) -> None:
        if self.id_type not in ["string", "integer"]:
            raise SchemaError("Must be 'string' or 'integer'", path + "id_type")
        if self.id_type == "integer":
            self.id_data_type = cd2t.types.integer.Integer()
        super().verify_options(path)

    def verify_data(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        findings = FindingsList()
        if self.minimum and len(data) < self.minimum:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"Attribute count is lower than minimum {self.minimum}",
                )
            )
        elif self.maximum is not None and len(data) > self.maximum:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"Attribute count is greater than maximum {self.maximum}",
                )
            )

        if path:
            path = path + "."
        for _id, element in data.items():
            _findings = FindingsList()
            _id_path = path + str(_id)
            _findings += self.id_data_type.validate_data(
                data=_id, path=_id_path, RTE=RTE
            )
            if (
                self.id_type == "integer"
                and self.allowed_ids
                # pylint: disable-next=unsupported-membership-test
                and _id not in self.allowed_ids
            ):
                _findings.append(
                    WrongValueFinding(
                        path=_id_path, message="Attribute is not an allowed value"
                    )
                )
            if not _findings:
                findings += self.element_type.validate_data(
                    data=element, path=_id_path, RTE=RTE
                )
            else:
                findings += _findings
        return findings

    def verify_reference(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        if not self.data_matches_type(data) or OPT.NONE in self.ref_OPT:
            return []
        if path:
            path = path + "."
        results = []
        for _id in data.keys():
            _id_path = path + str(_id)
            element = ReferenceElement(self.ref_key, _id_path, _id, self.ref_OPT)
            other = RTE.references.same_unique(element)
            if other is not None:
                if RTE.namespace != other.namespace:
                    _path = f"{other.namespace} > {other.path}"
                else:
                    _path = other.path
                results.append(
                    UniqueErrorFinding(
                        path=_id_path, message=f"ID already used at '{_path}'"
                    )
                )
            else:
                RTE.references.add_element(element)
        return results


class IDList_V2(IDList):
    V1_options = [
        # option_name, required, class
        ("id", False, (dict, str), "string"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.options.extend(self.V1_options)
        self.id = "string"
        self.id_data_type = cd2t.types.string.String()

    def build_schema(
        self,
        schema_definition: dict,
        path: str,
        RTE: RunTimeEnv,
        schema: cd2t.schema.Schema,
    ) -> cd2t.types.base.DataType:
        super().build_schema(
            schema_definition=schema_definition,
            path=path,
            RTE=RTE,
            schema=schema,
        )
        self.id_data_type = cd2t.types.parser.ParserDataType().build_schema(
            schema_definition=self.id,
            path=path + ".id",
            RTE=RTE,
            schema=schema,
        )
        return self

    def verify_data(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        findings = FindingsList()
        if self.minimum and len(data) < self.minimum:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"Attribute count is lower than minimum {self.minimum}",
                )
            )
        elif self.maximum is not None and len(data) > self.maximum:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"Attribute count is greater than maximum {self.maximum}",
                )
            )

        if path:
            path = path + "."
        for _id, element in data.items():
            _findings = FindingsList()
            _id_path = path + str(_id)
            _findings += self.id_data_type.validate_data(
                data=_id, path=_id_path, RTE=RTE
            )
            if not _findings:
                findings += self.element_type.validate_data(
                    data=element, path=_id_path, RTE=RTE
                )
            else:
                findings += _findings
        return findings
