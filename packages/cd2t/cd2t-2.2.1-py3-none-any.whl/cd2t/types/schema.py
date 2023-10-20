"""
Schema Data Type Class (for Schema Version 1)
"""
from cd2t.errors import SchemaError
from cd2t.run_time_env import RunTimeEnv
import cd2t.schema
import cd2t.types.base
import cd2t.types.parser


class SchemaDataType(cd2t.types.base.BaseDataType):
    data_type_name = "schema"
    options = [
        # option_name, required, class
        ("subschema", True, str, ""),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.subschema = ""
        self.sub_root_schema = None

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
        _sub_schema = RTE.subschemas.get(self.subschema, None)
        if _sub_schema is None:
            raise SchemaError(f"Could not found subschema '{self.subschema}'", path)
        new_path = path + "<" + self.subschema + ">"
        if self.subschema in RTE.subschema_path:
            raise SchemaError(
                f"Subschema loop detected {' -> '.join(RTE.subschema_path + [self.subschema])}",
                new_path,
            )

        if isinstance(_sub_schema, cd2t.schema.Schema):
            # Subschema was already build.
            return _sub_schema.root_data_type

        RTE.subschema_path.append(self.subschema)
        new_path = new_path + "root"
        self.sub_root_schema = _sub_schema.get("root", None)
        if self.sub_root_schema is None:
            raise SchemaError("Key missing", new_path)
        sub_data_obj = cd2t.types.parser.ParserDataType().build_schema(
            schema_definition=self.sub_root_schema,
            path=new_path,
            RTE=RTE,
            schema=schema,
        )
        sub_schema = cd2t.schema.Schema()
        sub_schema.set_root_data_type(sub_data_obj)
        RTE.subschemas[self.subschema] = sub_schema

        # Clean subschema_path
        RTE.subschema_path.pop()

        return sub_data_obj
