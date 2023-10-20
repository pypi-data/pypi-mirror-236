"""
Hostname Data Type Class
"""
from cd2t.errors import SchemaError
from cd2t.results import FindingsList, WrongValueFinding
from cd2t.run_time_env import RunTimeEnv
import cd2t.types.base
from cd2t.utils import string_matches_regex_list


class Hostname(cd2t.types.base.BaseDataType):
    customizable = True
    data_type_name = "hostname"
    matching_classes = [str]
    support_reference = True
    options = [
        # option_name, required, class, default_value
        ("maximum", False, int, 63),
        ("minimum", False, int, 1),
        ("allowed_values", False, list, None),
        ("not_allowed_values", False, list, []),
        ("strict_lower", False, bool, True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.minimum = 1
        self.maximum = 63
        self.allowed_values = None
        self.not_allowed_values = []
        self.strict_lower = True

    def verify_options(self, path: str):
        super().verify_options(path)
        i = 0
        for string in self.not_allowed_values:
            if not isinstance(string, str):
                raise SchemaError("Must be string", f"{path}not_allowed_values[{i}]")
            i += 1
        if self.allowed_values is not None:
            i = 0
            for string in self.allowed_values:
                if not isinstance(string, str):
                    raise SchemaError("Must be string", f"{path}allowed_values[{i}]")
                i += 1
        if not 0 < self.minimum < 64:
            raise SchemaError("Must be >0 and <64", path + "minimum")
        if not self.minimum < self.maximum < 64:
            raise SchemaError("Must be >'minimum' and <64", path + "maximum")

    def verify_data(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        findings = FindingsList()

        # Check for invalid characters
        hostname_len = len(data)
        first_char = 0
        last_char = hostname_len - 1
        for i in range(hostname_len):
            char = data[i]
            if self.strict_lower and char.isupper():
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"Hostname '{data}' contains upper case at position {i + 1}",
                    )
                )
            if i == first_char and not char.isalnum():
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message="Hostname must start with alphanumeric character",
                    )
                )
            elif i == last_char and not char.isalnum():
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message="Hostname must end with alphanumeric character",
                    )
                )
            elif not char.isalnum() and char != "-":
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"Hostname '{data}' contains illegal character at position {i + 1}",
                    )
                )

        # Check min and max length
        if self.minimum is not None and self.minimum > len(data):
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"Hostname length is lower than minimum {self.minimum}",
                )
            )
        elif self.maximum is not None and self.maximum < len(data):
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"Hostname length is greater than maximum {self.maximum}",
                )
            )

        # Check regex values
        matches = string_matches_regex_list(data, self.not_allowed_values)
        if matches:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"Hostname matches not allowed regex '{matches}'",
                )
            )
        elif self.allowed_values is not None:
            if not string_matches_regex_list(data, self.allowed_values):
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message="String does not match any allowed regex strings",
                    )
                )
        return findings
