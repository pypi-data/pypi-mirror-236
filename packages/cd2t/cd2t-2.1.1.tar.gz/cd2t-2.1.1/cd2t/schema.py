"""
Schema Class
"""
from cd2t.types.datatype import DataType


class Schema(dict):
    def __init__(
        self,
        root_data_type: DataType = None,
        version: int = 1,
        description: str = "",
        allow_shortcuts=False,
    ) -> None:
        super().__init__()
        self.root_data_type = root_data_type
        self.version = version
        self.allow_shortcuts = allow_shortcuts
        self.description = description
        self.custom_data_types = {}
        self.subschemas = {}
        if root_data_type is not None:
            self._check_rdt(root_data_type)

    @staticmethod
    def _check_rdt(rdt: DataType):
        if not issubclass(type(rdt), DataType):
            raise ValueError(
                f"Parameter 'root_data_type' is not a subclass to '{DataType}'"
            )

    def set_root_data_type(self, root_data_type):
        self._check_rdt(root_data_type)
        self.root_data_type = root_data_type
