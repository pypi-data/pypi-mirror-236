"""
cd2t error classes
"""


class SchemaError(ValueError):
    def __init__(self, message: str, path="") -> None:
        super().__init__()
        self.path = path
        self.message = message

    def __str__(self):
        if self.path:
            return f"{self.path}: {self.message}"
        return self.message
