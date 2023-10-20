"""
Enum Data Type Class
"""
from cd2t.errors import SchemaError
from cd2t.results import WrongValueFinding, FindingsList
from cd2t.run_time_env import RunTimeEnv
import cd2t.types.base


class Enum(cd2t.types.base.BaseDataType):
    customizable = True
    data_type_name = "enum"
    options = [
        # option_name, required, class
        ("allowed_values", True, list, None),
    ]
    supported_data_types = [int, float, dict, list, str]

    def __init__(self) -> None:
        super().__init__()
        self.matching_classes = []
        self.allowed_values = []
        self.data_type_mismatch_message = "None of the allowed value data types matches"

    def verify_options(self, path: str):
        if not self.allowed_values:
            raise SchemaError("Empty list not allowed", path + "allowed_values")
        i = 0
        for value in self.allowed_values:
            value_type = type(value)
            if value_type not in self.supported_data_types:
                raise SchemaError(
                    "contains unsupported data types",
                    f"{path}allowed_values[{i}]",
                )
            if value_type not in self.matching_classes:
                self.matching_classes.append(value_type)
            i += 1
        super().verify_options(path)

    def verify_data(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        findings = FindingsList()
        if data not in self.allowed_values:
            findings.append(WrongValueFinding(path=path, message="Value not allowed"))
        return findings
