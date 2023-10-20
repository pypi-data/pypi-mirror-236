"""
Parser Class (Helper for DT identification)
"""
from hashlib import sha1
from typing import Union
import copy
from cd2t.errors import SchemaError
import cd2t.run_time_env
import cd2t.schema
import cd2t.types.base
import cd2t.types.bool
import cd2t.types.datatype
import cd2t.types.enum
import cd2t.types.float
import cd2t.types.fqdn
import cd2t.types.hostname
import cd2t.types.idlist
import cd2t.types.integer
import cd2t.types.ip
import cd2t.types.list
import cd2t.types.multitype
import cd2t.types.none
import cd2t.types.object
import cd2t.types.schema
import cd2t.types.string
from cd2t.utils import merge_template_data

BUILTIN_DATA_TYPES = {
    1: {
        "any": cd2t.types.base.BaseDataType,
        "bool": cd2t.types.bool.Bool,
        "enum": cd2t.types.enum.Enum,
        "float": cd2t.types.float.Float,
        "idlist": cd2t.types.idlist.IDList_V1,
        "integer": cd2t.types.integer.Integer,
        "list": cd2t.types.list.List,
        "multitype": cd2t.types.multitype.Multitype,
        "none": cd2t.types.none.NoneDataType,
        "object": cd2t.types.object.Object_V1,
        "schema": cd2t.types.schema.SchemaDataType,
        "string": cd2t.types.string.String,
    },
    2: {
        "any": cd2t.types.base.BaseDataType,
        "bool": cd2t.types.bool.Bool,
        "enum": cd2t.types.enum.Enum,
        "float": cd2t.types.float.Float,
        "fqdn": cd2t.types.fqdn.FQDN,
        "hostname": cd2t.types.hostname.Hostname,
        "idlist": cd2t.types.idlist.IDList_V2,
        "integer": cd2t.types.integer.Integer,
        "ip": cd2t.types.ip.IP,
        "ip_address": cd2t.types.ip.IP_Address,
        "ip_network": cd2t.types.ip.IP_Network,
        "ip_interface": cd2t.types.ip.IP_Interface,
        "list": cd2t.types.list.List,
        "multitype": cd2t.types.multitype.Multitype,
        "none": cd2t.types.none.NoneDataType,
        "object": cd2t.types.object.Object_V2,
        "string": cd2t.types.string.String,
    },
}


class ParserDataType:
    # pylint: disable=too-few-public-methods
    def build_schema(
        self,
        schema_definition: Union[dict, str],
        path: int,
        RTE: cd2t.run_time_env.RunTimeEnv,  # pylint: disable=invalid-name
        schema: cd2t.schema.Schema = cd2t.schema.Schema(),
    ) -> cd2t.types.datatype.DataType:
        template = None
        if isinstance(schema_definition, dict):
            schema_definition = schema_definition.copy()
            if len(schema_definition) == 0:
                return BUILTIN_DATA_TYPES[schema.version]["any"]()
            if schema.version == 2:
                template = schema_definition.pop("template", None)
                if template:
                    if template not in RTE.templates.keys():
                        raise SchemaError(
                            path=path, message=f"Template '{template}' not found"
                        )
                    template_merge_options = schema_definition.pop(
                        "template_merge_options", {}
                    )
                    recursive = template_merge_options.get(
                        "recursive", RTE.templates_merge_recursive
                    )
                    list_merge = template_merge_options.get(
                        "list_merge", RTE.templates_list_merge
                    )
                    schema_definition = merge_template_data(
                        template_data=copy.deepcopy(RTE.templates[template]),
                        additional_data=schema_definition,
                        recursive=recursive,
                        list_merge=list_merge,
                    )
                    hash_obj = sha1()
                    hash_obj.update(str(schema_definition).encode())
                    schema_hash = hash_obj.hexdigest()
                    if schema_hash in RTE.template_hash_stack:
                        raise SchemaError(path=path, message="Template looping")
                    RTE.template_hash_stack.append(schema_hash)
            data_type_name = schema_definition.pop("type", None)
            if data_type_name is None:
                raise SchemaError("Needs to have a key 'type'", path)
        elif schema.allow_shortcuts and isinstance(schema_definition, str):
            data_type_name = schema_definition
            schema_definition = {}
        else:
            raise SchemaError("Wrong value type", path)

        if data_type_name in schema.custom_data_types.keys():
            schema_definition_copy = schema_definition
            schema_definition = schema.custom_data_types[data_type_name].copy()
            schema_definition.update(schema_definition_copy)
            data_type_name = schema_definition.pop("type", None)

        data_type_class = BUILTIN_DATA_TYPES[schema.version].get(data_type_name, None)
        if data_type_class is None:
            raise SchemaError(f"Data type '{data_type_name}' not found", path)

        data_type_obj = data_type_class().build_schema(
            schema_definition=schema_definition,
            path=path,
            RTE=RTE,
            schema=schema,
        )

        if template:
            RTE.template_hash_stack.pop()

        return data_type_obj
