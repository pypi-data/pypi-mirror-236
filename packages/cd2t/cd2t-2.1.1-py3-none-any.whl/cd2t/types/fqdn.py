"""
FQDN Data Type Class
"""
import re
from cd2t.errors import SchemaError
from cd2t.results import FindingsList, WrongValueFinding
from cd2t.run_time_env import RunTimeEnv
import cd2t.types.base
from cd2t.types.hostname import Hostname
from cd2t.utils import string_matches_regex_list


class FQDN(cd2t.types.base.BaseDataType):
    customizable = True
    data_type_name = "fqdn"
    matching_classes = [str]
    support_reference = True
    options = [
        # option_name, required, class, default_value
        ("maximum", False, int, 255),
        ("minimum", False, int, 1),
        ("minimum_labels", False, int, 2),
        ("maximum_labels", False, int, None),
        ("allowed_values", False, list, None),
        ("not_allowed_values", False, list, []),
        ("strict_lower", False, bool, True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.minimum = 4
        self.maximum = 255
        self.minimum_labels = 2
        self.maximum_labels = None
        self.allowed_values = None
        self.not_allowed_values = []
        self.strict_lower = True

    def verify_options(self, path: str):
        super().verify_options(path)
        i = 0
        for string in self.not_allowed_values:
            if not isinstance(string, str):
                raise SchemaError("Must be string", f"{path}not_allowed_values[{i}]")
            try:
                re.compile(string)
            except re.error as exc:
                raise SchemaError(
                    f"'{i}' is not a valid regex string",
                    f"{path}not_allowed_values[{i}]",
                ) from exc
            i += 1
        if self.allowed_values is not None:
            i = 0
            for string in self.allowed_values:
                if not isinstance(string, str):
                    raise SchemaError("Must be string", f"{path}allowed_values[{i}]")
                try:
                    re.compile(string)
                except re.error as exc:
                    raise SchemaError(
                        f"'{string}' is not a valid regex string",
                        f"{path}allowed_values[{i}]",
                    ) from exc
                i += 1
        if not 4 <= self.minimum <= 255:
            raise SchemaError("Must be >=4 and <=255", path + "minimum")
        if not self.minimum <= self.maximum <= 255:
            raise SchemaError("Must be >='minimum' and <=255", path + "maximum")
        if 2 > self.minimum_labels:
            raise SchemaError("Must be >=2", path + "minimum_labels")
        if (
            self.maximum_labels is not None
            and self.minimum_labels > self.maximum_labels
        ):
            raise SchemaError("Must be >='minimum_labels'", path + "maximum_labels")

    def verify_data(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        # pylint: disable=too-many-branches,too-many-locals
        findings = FindingsList()

        # Check min and max length
        if self.minimum > len(data):
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"FQDN length is lower than minimum {self.minimum}",
                )
            )
        elif self.maximum < len(data):
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"FQDN length is greater than maximum {self.maximum}",
                )
            )

        # Split hostname and labels and verify label count
        labels = data.split(".")
        if len(labels) < 2:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"'{data}' is not a valid FQDN",
                )
            )
            return findings

        label_count = len(labels)
        hostname = labels[0]
        domain_labels = labels[1:]

        if label_count < self.minimum_labels:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"'{data}' label count of {label_count} is lower "
                    + f"than minimum {self.minimum_labels}",
                )
            )
        elif self.maximum_labels is not None and label_count > self.maximum_labels:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"'{data}' label count of {label_count} is higher "
                    + f"than maximum {self.maximum_labels}",
                )
            )

        # Verify hostname part
        h_obj = Hostname()
        h_obj.strict_lower = self.strict_lower
        findings += h_obj.validate_data(data=hostname, path=path, RTE=RTE)

        # Check each domain label:
        position = len(hostname) + 2  # starting at first char behind first 'dot'
        for label in domain_labels:
            first_char = 0
            last_char = len(label) - 1
            for i, char in enumerate(label):
                if self.strict_lower and char.isupper():
                    findings.append(
                        WrongValueFinding(
                            path=path,
                            message=f"FQDN '{data}' contains upper case at "
                            + f"position {position}",
                        )
                    )
                if i == first_char and not char.isalpha():
                    findings.append(
                        WrongValueFinding(
                            path=path,
                            message=f"FQDN '{data}' domain labels must start with an "
                            + "alphabetic character",
                        )
                    )
                elif i == last_char and not char.isalnum():
                    findings.append(
                        WrongValueFinding(
                            path=path,
                            message=f"FQDN '{data}' domain labels must end with an "
                            + "alphanumeric character",
                        )
                    )
                elif not char.isalnum() and char != "-":
                    findings.append(
                        WrongValueFinding(
                            path=path,
                            message=f"FQDN '{data}' contains illegal character "
                            + f"at position {position + 1}",
                        )
                    )
            position += len(label) + 1

        # Check regex values
        matches = string_matches_regex_list(data, self.not_allowed_values)
        if matches:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"FQDN '{data}' matches not allowed regex '{matches}'",
                )
            )
        elif self.allowed_values is not None:
            if not string_matches_regex_list(data, self.allowed_values):
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"FQDN '{data}' does not match any allowed regex strings",
                    )
                )

        return findings
