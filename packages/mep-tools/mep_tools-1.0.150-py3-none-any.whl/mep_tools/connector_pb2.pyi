from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DispatcherRequest(_message.Message):
    __slots__ = ["payload"]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: _struct_pb2.Value
    def __init__(self, payload: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...

class DispatcherResponse(_message.Message):
    __slots__ = ["payload"]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: _struct_pb2.ListValue
    def __init__(self, payload: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ...) -> None: ...
