"""
List Data Type Class
"""
import copy
from cd2t.results import FindingsList, ValidationFinding, WrongValueFinding
from cd2t.run_time_env import RunTimeEnv
import cd2t.schema
import cd2t.types.base
import cd2t.types.parser


class List(cd2t.types.base.BaseDataType):
    data_type_name = "list"
    matching_classes = [list]
    options = [
        # option_name, required, class
        ("minimum", False, int, None),
        ("maximum", False, int, None),
        ("allow_duplicates", False, bool, True),
        ("elements", True, [dict, str], {}),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.minimum = None
        self.maximum = None
        self.allow_duplicates = True
        self.elements = {}
        self.element_data_type = None

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
        self.element_data_type = cd2t.types.parser.ParserDataType().build_schema(
            schema_definition=self.elements,
            path=path + ".elements",
            RTE=RTE,
            schema=schema,
        )
        return self

    def build_sub_references(self, data: any, path: str, RTE: RunTimeEnv):
        i = 0
        for element in data:
            self.element_data_type.build_references(element, f"{path}[{i}]", RTE)
            i += 1

    def autogenerate_data(self, data: any, path: str, RTE: RunTimeEnv):
        findings = FindingsList()
        if not self.data_matches_type(data):
            return data, findings
        for i, element in enumerate(data):
            _data, _findings = self.element_data_type.autogenerate_data(
                element, f"{path}[{i}]", RTE
            )
            data[i] = _data
            findings += _findings
        return data, findings

    def verify_data(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        findings = FindingsList()
        if self.minimum and len(data) < self.minimum:
            findings.append(
                WrongValueFinding(
                    path=path, message=f"Length of list is lower than {self.minimum}"
                )
            )
        elif self.maximum and len(data) > self.maximum:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"Length of list is greater than {self.maximum}",
                )
            )
        i = 0
        for element in data:
            findings += self.element_data_type.validate_data(
                element, f"{path}[{i}]", RTE
            )
            i += 1

        if not self.allow_duplicates:
            remaining_data = copy.copy(data)
            i = 0
            for element in data:
                remaining_data = remaining_data[1:]
                if element in remaining_data:
                    relative_position = remaining_data.index(element) + 1
                    findings.append(
                        ValidationFinding(
                            path=f"{path}[{i}]",
                            message=f"Element is same as on position {i + relative_position}",
                        )
                    )
                i += 1
        return findings
