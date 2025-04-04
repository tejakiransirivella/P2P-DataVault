from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LookupRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class LookupResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TestRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class TestResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class FindRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class FindNodeResponse(_message.Message):
    __slots__ = ("ip_address", "udp_port", "node_id")
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UDP_PORT_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    ip_address: str
    udp_port: str
    node_id: str
    def __init__(self, ip_address: _Optional[str] = ..., udp_port: _Optional[str] = ..., node_id: _Optional[str] = ...) -> None: ...

class FindValueResponse(_message.Message):
    __slots__ = ("find_node_res", "value")
    FIND_NODE_RES_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    find_node_res: FindNodeResponse
    value: str
    def __init__(self, find_node_res: _Optional[_Union[FindNodeResponse, _Mapping]] = ..., value: _Optional[str] = ...) -> None: ...

class StoreRequest(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class StoreResponse(_message.Message):
    __slots__ = ("is_stored",)
    IS_STORED_FIELD_NUMBER: _ClassVar[int]
    is_stored: bool
    def __init__(self, is_stored: bool = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
