"""
Multitype Data Type Class
"""
from cd2t.errors import SchemaError
from cd2t.references import ReferenceFinding
from cd2t.results import DataTypeMismatch, FindingsList
from cd2t.run_time_env import RunTimeEnv
import cd2t.schema
import cd2t.types.base
import cd2t.types.parser


class Multitype(cd2t.types.base.BaseDataType):
    data_type_name = "multitype"
    options = [
        # option_name, required, class
        ("types", True, list, None),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.types = []
        self.type_objects = []
        self.matching_classes = []
        self.data_type_mismatch_message = "None of the data types matches"

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
        i = 0
        for _type in self.types:
            _path = f"{path}.types[{i}]"
            data_type = cd2t.types.parser.ParserDataType().build_schema(
                schema_definition=_type, path=_path, RTE=RTE, schema=schema
            )
            if data_type.data_type_name == self.data_type_name:
                raise SchemaError("Multitype in Multitype not supported", _path)
            self.type_objects.append(data_type)
            self.matching_classes.extend(data_type.matching_classes)
            i += 1
        return self

    def build_sub_references(self, data: any, path: str, RTE: RunTimeEnv) -> list:
        for type_object in self.type_objects:
            if type_object.data_matches_type(data):
                type_object.build_references(data=data, path=path, RTE=RTE)

    def autogenerate_data(self, data: any, path: str, RTE: RunTimeEnv):
        findings = FindingsList()
        if data is None:
            return data, findings
        # Try to find ...
        for type_object in self.type_objects:
            if type_object.data_matches_type:
                findings += type_object.autogenerate_data(data=data, path=path, RTE=RTE)
        return data, findings

    def validate_data(self, data: any, path: str, RTE=RunTimeEnv) -> list:
        findings = FindingsList()
        near_finding_found = False
        for type_object in self.type_objects:
            # New data path syntax prevents analysis if finding is comming from sub data type.
            _findings = type_object.validate_data(data=data, path=path, RTE=RTE)
            if not _findings:
                return _findings
            if not near_finding_found and isinstance(_findings[0], ReferenceFinding):
                findings = _findings
        if not findings:
            findings.append(
                DataTypeMismatch(path=path, message="None of the data types matches")
            )
        return findings
