from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetVariablesRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetVariablesResponse(_message.Message):
    __slots__ = ("variables",)
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    variables: _containers.RepeatedCompositeFieldContainer[Variable]
    def __init__(self, variables: _Optional[_Iterable[_Union[Variable, _Mapping]]] = ...) -> None: ...

class Variable(_message.Message):
    __slots__ = ("id", "name", "is_system", "entity")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    is_system: bool
    entity: Entity
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., is_system: bool = ..., entity: _Optional[_Union[Entity, _Mapping]] = ...) -> None: ...

class Entity(_message.Message):
    __slots__ = ("name", "options")
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    options: _containers.RepeatedCompositeFieldContainer[Option]
    def __init__(self, name: _Optional[str] = ..., options: _Optional[_Iterable[_Union[Option, _Mapping]]] = ...) -> None: ...

class Option(_message.Message):
    __slots__ = ("name", "synonyms")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYNONYMS_FIELD_NUMBER: _ClassVar[int]
    name: str
    synonyms: _containers.RepeatedCompositeFieldContainer[Synonym]
    def __init__(self, name: _Optional[str] = ..., synonyms: _Optional[_Iterable[_Union[Synonym, _Mapping]]] = ...) -> None: ...

class Synonym(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
