"""
IP Data Type Classes
"""
# pylint: disable=unused-argument,invalid-name
import ipaddress
from cd2t.errors import SchemaError
from cd2t.results import FindingsList, WrongValueFinding
from cd2t.run_time_env import RunTimeEnv
import cd2t.types.base


class IP(cd2t.types.base.BaseDataType):
    # pylint: disable=too-many-instance-attributes
    customizable = True
    data_type_name = "ip"
    matching_classes = [str]
    support_reference = True
    options = [
        # option_name, required, class, default_value
        ("loopback", False, bool, None),
        ("version", False, int, None),
        ("link_local", False, bool, None),
        ("private", False, bool, None),
        ("public", False, bool, None),
        ("multicast", False, bool, None),
        ("allowed_values", False, list, None),
        ("not_allowed_values", False, list, []),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.loopback = None
        self.version = None
        self.link_local = None
        self.private = None
        self.public = None
        self.multicast = None
        self.allowed_values = None
        self.not_allowed_values = []

    def verify_options(self, path: str):
        super().verify_options(path)
        if self.version is not None and self.version not in [4, 6]:
            raise SchemaError(
                path=path + "version", message="Version must either 4 or 6"
            )
        i = 0
        for string in self.not_allowed_values:
            if isinstance(string, str):
                try:
                    _ip = ipaddress.ip_interface(string)
                except ValueError as exc:
                    raise SchemaError(
                        "Must be an IP object",
                        f"{path}not_allowed_values[{i}]",
                    ) from exc
            else:
                raise SchemaError(
                    "Must be an IP object",
                    f"{path}not_allowed_values[{i}]",
                )
            if self.version is not None and _ip.version != self.version:
                raise SchemaError(
                    path=f"{path}not_allowed_values[{i}]",
                    message=f"Must be an object of IP version {self.version}",
                )
            i += 1
        if self.allowed_values is not None:
            i = 0
            for string in self.allowed_values:
                if isinstance(string, str):
                    try:
                        _ip = ipaddress.ip_interface(string)
                    except ValueError as exc:
                        raise SchemaError(
                            "Must be an IP object",
                            f"{path}allowed_values[{i}]",
                        ) from exc
                else:
                    raise SchemaError(
                        "Must be an IP object",
                        f"{path}allowed_values[{i}]",
                    )
                if self.version is not None and _ip.version != self.version:
                    raise SchemaError(
                        path=f"{path}allowed_values[{i}]",
                        message=f"Must be an object of IP version {self.version}",
                    )
                i += 1

    def verify_ip_object_type(self, data: any, path: str):
        findings = FindingsList()
        ip_obj = None
        try:
            ip_obj = ipaddress.ip_address(data)
        except ValueError:
            pass
        try:
            ip_obj = ipaddress.ip_network(data)
        except ValueError:
            pass
        try:
            ip_obj = ipaddress.ip_interface(data)
        except ValueError:
            pass
        if ip_obj is None:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message="Data not an IP object",
                )
            )
        return findings, ip_obj

    def verify_data(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        # pylint: disable=too-many-branches
        findings, ip_obj = self.verify_ip_object_type(data=data, path=path)
        if ip_obj is None:
            return findings

        if self.version is not None and ip_obj.version != self.version:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"{data} is not IP version {self.version}",
                )
            )

        if self.loopback is not None:
            if self.loopback and not ip_obj.is_loopback:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"{data} is not a loopback",
                    )
                )
            if not self.loopback and ip_obj.is_loopback:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"{data} mustn't be a loopback",
                    )
                )

        if self.link_local is not None:
            if self.link_local and not ip_obj.is_link_local:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"{data} is not link local",
                    )
                )
            if not self.link_local and ip_obj.is_link_local:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"{data} mustn't be link local",
                    )
                )

        if self.private is not None:
            if self.private and not ip_obj.is_private:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"{data} is not private",
                    )
                )
            if not self.private and ip_obj.is_private:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"{data} mustn't be private",
                    )
                )

        if self.public is not None:
            if self.public and not ip_obj.is_global:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"{data} is not public",
                    )
                )
            if not self.public and ip_obj.is_global:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"{data} mustn't be public",
                    )
                )

        if self.multicast is not None:
            if self.multicast and not ip_obj.is_multicast:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"{data} is not multicast",
                    )
                )
            if not self.multicast and ip_obj.is_multicast:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"{data} mustn't be multicast",
                    )
                )

        if data in self.not_allowed_values:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"IP object matches not allowed IP object '{data}'",
                )
            )
        # pylint: disable-next=unsupported-membership-test
        if self.allowed_values and data not in self.allowed_values:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"IP object '{data}' matches none of the allowed IP objects",
                )
            )

        return findings


class __IP_Specialized(IP):
    options_special = [
        # option_name, required, class, default_value
        ("allowed_subnets", False, list, None),
        ("not_allowed_subnets", False, list, []),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.allowed_subnets = None
        self.not_allowed_subnets = []
        self.options = self.options + self.options_special

    def verify_options(self, path: str):
        super().verify_options(path)
        i = 0
        for string in self.not_allowed_subnets:
            if isinstance(string, str):
                try:
                    _ip = ipaddress.ip_network(string)
                except ValueError as exc:
                    raise SchemaError(
                        "Must be an IP subnet", f"{path}not_allowed_subnets[{i}]"
                    ) from exc
            else:
                raise SchemaError(
                    "Must be an IP subnet", f"{path}not_allowed_subnets[{i}]"
                )
            if self.version is not None and _ip.version != self.version:
                raise SchemaError(
                    path=f"{path}not_allowed_subnets[{i}]",
                    message=f"Must be an IP version {self.version} subnet",
                )
            i += 1
        if self.allowed_subnets is not None:
            i = 0
            for string in self.allowed_subnets:
                if isinstance(string, str):
                    try:
                        _ip = ipaddress.ip_network(string)
                    except ValueError as exc:
                        raise SchemaError(
                            "Must be an IP subnet", f"{path}allowed_subnets[{i}]"
                        ) from exc
                else:
                    raise SchemaError(
                        "Must be an IP subnet", f"{path}allowed_subnets[{i}]"
                    )
                if self.version is not None and _ip.version != self.version:
                    raise SchemaError(
                        path=f"{path}allowed_subnets[{i}]",
                        message=f"Must be an IP version {self.version} subnet",
                    )
                i += 1

    def verify_ip_object_type(self, data: any, path: str):
        return FindingsList(), None

    def verify_subnets(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        return FindingsList()

    def verify_with_special_type_options(
        self, data: any, path: str, RTE: RunTimeEnv
    ) -> FindingsList:
        return FindingsList()

    def verify_data(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        findings = super().verify_data(data=data, path=path, RTE=RTE)
        if not findings:
            findings = self.verify_subnets(data=data, path=path, RTE=RTE)
            findings += self.verify_with_special_type_options(
                data=data, path=path, RTE=RTE
            )
        return findings


class IP_Address(__IP_Specialized):
    data_type_name = "ip_address"

    def verify_ip_object_type(self, data: any, path: str):
        findings = FindingsList()
        ip_obj = None
        try:
            ip_obj = ipaddress.ip_address(data)
        except ValueError:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message="Data not an IP address",
                )
            )
        return findings, ip_obj

    def verify_subnets(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        findings = FindingsList()
        ip_obj = ipaddress.ip_address(data)

        for subnet in self.not_allowed_subnets:
            subnet_obj = ipaddress.ip_network(subnet)
            if ip_obj in subnet_obj:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"IP address '{data}' within not allowed IP subnet '{subnet}'",
                    )
                )
        if self.allowed_subnets is not None:
            match = False
            for subnet in self.allowed_subnets:
                subnet_obj = ipaddress.ip_network(subnet)
                if ip_obj in subnet_obj:
                    match = True
                    break
            if not match:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"IP address '{data}' matches none of the allowed IP subnets",
                    )
                )

        return findings


class IP_Network(__IP_Specialized):
    data_type_name = "ip_network"
    options_network = [
        # option_name, required, class, default_value
        ("minimum_prefix_length", False, int, 0),
        ("maximum_prefix_length", False, int, None),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.minimum_prefix_length = 0
        self.maximum_prefix_length = None
        self.options = self.options + self.options_network

    def verify_options(self, path: str):
        super().verify_options(path)
        if self.version == 4:
            if self.minimum_prefix_length > 32:
                raise SchemaError(
                    "Must be <= 32 for IP version 4",
                    path + "minimum_prefix_length",
                )
            if self.maximum_prefix_length is not None:
                if self.minimum_prefix_length > self.maximum_prefix_length:
                    raise SchemaError(
                        "Must be >= 'minimum_prefix_length'",
                        path + "maximum_prefix_length",
                    )
                if self.maximum_prefix_length > 32:
                    raise SchemaError(
                        "Must be <= 32 for IP version 4",
                        path + "maximum_prefix_length",
                    )

        else:
            if self.minimum_prefix_length > 128:
                raise SchemaError("Must be <= 128", path + "minimum_prefix_length")
            if self.maximum_prefix_length is not None:
                if self.minimum_prefix_length > self.maximum_prefix_length:
                    raise SchemaError(
                        "Must be >= 'minimum_prefix_length'",
                        path + "maximum_prefix_length",
                    )
                if self.maximum_prefix_length > 128:
                    raise SchemaError("Must be <= 128", path + "maximum_prefix_length")

    def verify_ip_object_type(self, data: any, path: str):
        findings = FindingsList()
        ip_obj = None
        try:
            ip_obj = ipaddress.ip_network(data)
        except ValueError:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message="Data not an IP network",
                )
            )
        return findings, ip_obj

    def verify_subnets(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        findings = FindingsList()
        ip_obj = ipaddress.ip_network(data)

        for subnet in self.not_allowed_subnets:
            subnet_obj = ipaddress.ip_network(subnet)
            if ip_obj.version == subnet_obj.version and ip_obj.subnet_of(subnet_obj):
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"IP network '{data}' within not allowed IP subnet '{subnet}'",
                    )
                )
        if self.allowed_subnets is not None:
            match = False
            for subnet in self.allowed_subnets:
                subnet_obj = ipaddress.ip_network(subnet)
                if ip_obj.version == subnet_obj.version and ip_obj.subnet_of(
                    subnet_obj
                ):
                    match = True
                    break
            if not match:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"IP network '{data}' matches none of the allowed IP subnets",
                    )
                )

        return findings

    def verify_with_special_type_options(
        self, data: any, path: str, RTE: RunTimeEnv
    ) -> FindingsList:
        findings = FindingsList()
        ip_obj = ipaddress.ip_network(data)
        if ip_obj.prefixlen < self.minimum_prefix_length:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"IP network '{data}' prefix length "
                    + f"is lower than minimum {self.minimum_prefix_length}",
                )
            )
        elif (
            self.maximum_prefix_length is not None
            and ip_obj.prefixlen > self.maximum_prefix_length
        ):
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"IP network '{data}' prefix length "
                    + f"is higher than maximum {self.maximum_prefix_length}",
                )
            )
        return findings


class IP_Interface(IP_Address):
    data_type_name = "ip_interface"

    def verify_ip_object_type(self, data: any, path: str):
        findings = FindingsList()
        ip_obj = None
        try:
            ip_obj = ipaddress.ip_interface(data)
        except ValueError:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message="Data not an IP interface",
                )
            )
        if "/" not in data:
            findings.append(
                WrongValueFinding(
                    path=path,
                    message=f"IP address '{data}' not an IP interface",
                )
            )
        return findings, ip_obj

    def verify_subnets(self, data: any, path: str, RTE: RunTimeEnv) -> FindingsList:
        findings = FindingsList()
        ip_obj = ipaddress.ip_interface(data)

        for subnet in self.not_allowed_subnets:
            subnet_obj = ipaddress.ip_network(subnet)
            if ip_obj in subnet_obj:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"IP interface '{data}' within not allowed IP subnet '{subnet}'",
                    )
                )
        if self.allowed_subnets is not None:
            match = False
            for subnet in self.allowed_subnets:
                subnet_obj = ipaddress.ip_network(subnet)
                if ip_obj in subnet_obj:
                    match = True
                    break
            if not match:
                findings.append(
                    WrongValueFinding(
                        path=path,
                        message=f"IP interface '{data}' matches none of the allowed IP subnets",
                    )
                )

        return findings
