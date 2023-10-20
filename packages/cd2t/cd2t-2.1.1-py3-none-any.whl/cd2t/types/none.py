"""
None Data Type Class
"""
import cd2t.types.base


class NoneDataType(cd2t.types.base.BaseDataType):
    customizable = True
    data_type_name = "none"

    def __init__(self) -> None:
        super().__init__()
        self.matching_classes.append(type(None))
