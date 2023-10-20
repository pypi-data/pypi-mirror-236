"""
RTE Class
"""
from cd2t.references import References


class RunTimeEnv:
    """Stores all information during loading schemas and data validations."""

    # pylint: disable=too-few-public-methods,too-many-instance-attributes

    def __init__(self, namespace: str = None) -> None:
        """
        Args:
            namespace: string - Initial namespace

            data_types: dictionary
                with data type name as key and data type class as value
        """
        self.references = References()
        self.namespace = ""
        if namespace is not None:
            self.change_namespace(namespace)
        self.subschemas = {}
        self.subschema_path = []
        self.templates = {}
        self.templates_merge_recursive = True
        self.templates_list_merge = "append_rp"
        self.template_hash_stack = []
        try:
            # pylint: disable-next=import-outside-toplevel
            from ruamel.yaml import CommentedMap, CommentedSeq

            self.ruamel_yaml_available = True
            self.ruamel_commented_map = CommentedMap
            self.ruamel_commented_seq = CommentedSeq
        except ImportError:
            self.ruamel_yaml_available = False

    def change_namespace(self, namespace: str) -> None:
        """
        Args:
            namespace: string - New namespace
        """
        if not isinstance(namespace, str):
            raise ValueError("namespace has to be a string")
        self.references.change_namespace(namespace)
        self.namespace = namespace
