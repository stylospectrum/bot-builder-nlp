from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import service as _service
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceMetadataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ServiceMetadataResponse(_message.Message):
    __slots__ = ("name", "apis", "docs")
    class DescriptorMetadata(_message.Message):
        __slots__ = ("descriptor_id", "attributes")
        DESCRIPTOR_ID_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        descriptor_id: str
        attributes: _struct_pb2.Struct
        def __init__(self, descriptor_id: _Optional[str] = ..., attributes: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    class InferenceAPI(_message.Message):
        __slots__ = ("name", "input", "output", "docs")
        NAME_FIELD_NUMBER: _ClassVar[int]
        INPUT_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_FIELD_NUMBER: _ClassVar[int]
        DOCS_FIELD_NUMBER: _ClassVar[int]
        name: str
        input: ServiceMetadataResponse.DescriptorMetadata
        output: ServiceMetadataResponse.DescriptorMetadata
        docs: str
        def __init__(self, name: _Optional[str] = ..., input: _Optional[_Union[ServiceMetadataResponse.DescriptorMetadata, _Mapping]] = ..., output: _Optional[_Union[ServiceMetadataResponse.DescriptorMetadata, _Mapping]] = ..., docs: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    APIS_FIELD_NUMBER: _ClassVar[int]
    DOCS_FIELD_NUMBER: _ClassVar[int]
    name: str
    apis: _containers.RepeatedCompositeFieldContainer[ServiceMetadataResponse.InferenceAPI]
    docs: str
    def __init__(self, name: _Optional[str] = ..., apis: _Optional[_Iterable[_Union[ServiceMetadataResponse.InferenceAPI, _Mapping]]] = ..., docs: _Optional[str] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ("api_name", "ndarray", "dataframe", "series", "file", "text", "json", "multipart", "serialized_bytes")
    API_NAME_FIELD_NUMBER: _ClassVar[int]
    NDARRAY_FIELD_NUMBER: _ClassVar[int]
    DATAFRAME_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    JSON_FIELD_NUMBER: _ClassVar[int]
    MULTIPART_FIELD_NUMBER: _ClassVar[int]
    SERIALIZED_BYTES_FIELD_NUMBER: _ClassVar[int]
    api_name: str
    ndarray: NDArray
    dataframe: DataFrame
    series: Series
    file: File
    text: _wrappers_pb2.StringValue
    json: _struct_pb2.Value
    multipart: Multipart
    serialized_bytes: bytes
    def __init__(self, api_name: _Optional[str] = ..., ndarray: _Optional[_Union[NDArray, _Mapping]] = ..., dataframe: _Optional[_Union[DataFrame, _Mapping]] = ..., series: _Optional[_Union[Series, _Mapping]] = ..., file: _Optional[_Union[File, _Mapping]] = ..., text: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., json: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., multipart: _Optional[_Union[Multipart, _Mapping]] = ..., serialized_bytes: _Optional[bytes] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("ndarray", "dataframe", "series", "file", "text", "json", "multipart", "serialized_bytes")
    NDARRAY_FIELD_NUMBER: _ClassVar[int]
    DATAFRAME_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    JSON_FIELD_NUMBER: _ClassVar[int]
    MULTIPART_FIELD_NUMBER: _ClassVar[int]
    SERIALIZED_BYTES_FIELD_NUMBER: _ClassVar[int]
    ndarray: NDArray
    dataframe: DataFrame
    series: Series
    file: File
    text: _wrappers_pb2.StringValue
    json: _struct_pb2.Value
    multipart: Multipart
    serialized_bytes: bytes
    def __init__(self, ndarray: _Optional[_Union[NDArray, _Mapping]] = ..., dataframe: _Optional[_Union[DataFrame, _Mapping]] = ..., series: _Optional[_Union[Series, _Mapping]] = ..., file: _Optional[_Union[File, _Mapping]] = ..., text: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., json: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., multipart: _Optional[_Union[Multipart, _Mapping]] = ..., serialized_bytes: _Optional[bytes] = ...) -> None: ...

class Part(_message.Message):
    __slots__ = ("ndarray", "dataframe", "series", "file", "text", "json", "serialized_bytes")
    NDARRAY_FIELD_NUMBER: _ClassVar[int]
    DATAFRAME_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    JSON_FIELD_NUMBER: _ClassVar[int]
    SERIALIZED_BYTES_FIELD_NUMBER: _ClassVar[int]
    ndarray: NDArray
    dataframe: DataFrame
    series: Series
    file: File
    text: _wrappers_pb2.StringValue
    json: _struct_pb2.Value
    serialized_bytes: bytes
    def __init__(self, ndarray: _Optional[_Union[NDArray, _Mapping]] = ..., dataframe: _Optional[_Union[DataFrame, _Mapping]] = ..., series: _Optional[_Union[Series, _Mapping]] = ..., file: _Optional[_Union[File, _Mapping]] = ..., text: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., json: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., serialized_bytes: _Optional[bytes] = ...) -> None: ...

class Multipart(_message.Message):
    __slots__ = ("fields",)
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Part
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Part, _Mapping]] = ...) -> None: ...
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.MessageMap[str, Part]
    def __init__(self, fields: _Optional[_Mapping[str, Part]] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ("kind", "content")
    KIND_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    kind: str
    content: bytes
    def __init__(self, kind: _Optional[str] = ..., content: _Optional[bytes] = ...) -> None: ...

class DataFrame(_message.Message):
    __slots__ = ("column_names", "columns")
    COLUMN_NAMES_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    column_names: _containers.RepeatedScalarFieldContainer[str]
    columns: _containers.RepeatedCompositeFieldContainer[Series]
    def __init__(self, column_names: _Optional[_Iterable[str]] = ..., columns: _Optional[_Iterable[_Union[Series, _Mapping]]] = ...) -> None: ...

class Series(_message.Message):
    __slots__ = ("bool_values", "float_values", "int32_values", "int64_values", "string_values", "double_values")
    BOOL_VALUES_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUES_FIELD_NUMBER: _ClassVar[int]
    INT32_VALUES_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUES_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUES_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    bool_values: _containers.RepeatedScalarFieldContainer[bool]
    float_values: _containers.RepeatedScalarFieldContainer[float]
    int32_values: _containers.RepeatedScalarFieldContainer[int]
    int64_values: _containers.RepeatedScalarFieldContainer[int]
    string_values: _containers.RepeatedScalarFieldContainer[str]
    double_values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, bool_values: _Optional[_Iterable[bool]] = ..., float_values: _Optional[_Iterable[float]] = ..., int32_values: _Optional[_Iterable[int]] = ..., int64_values: _Optional[_Iterable[int]] = ..., string_values: _Optional[_Iterable[str]] = ..., double_values: _Optional[_Iterable[float]] = ...) -> None: ...

class NDArray(_message.Message):
    __slots__ = ("dtype", "shape", "string_values", "float_values", "double_values", "bool_values", "int32_values", "int64_values", "uint32_values", "uint64_values")
    class DType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DTYPE_UNSPECIFIED: _ClassVar[NDArray.DType]
        DTYPE_FLOAT: _ClassVar[NDArray.DType]
        DTYPE_DOUBLE: _ClassVar[NDArray.DType]
        DTYPE_BOOL: _ClassVar[NDArray.DType]
        DTYPE_INT32: _ClassVar[NDArray.DType]
        DTYPE_INT64: _ClassVar[NDArray.DType]
        DTYPE_UINT32: _ClassVar[NDArray.DType]
        DTYPE_UINT64: _ClassVar[NDArray.DType]
        DTYPE_STRING: _ClassVar[NDArray.DType]
    DTYPE_UNSPECIFIED: NDArray.DType
    DTYPE_FLOAT: NDArray.DType
    DTYPE_DOUBLE: NDArray.DType
    DTYPE_BOOL: NDArray.DType
    DTYPE_INT32: NDArray.DType
    DTYPE_INT64: NDArray.DType
    DTYPE_UINT32: NDArray.DType
    DTYPE_UINT64: NDArray.DType
    DTYPE_STRING: NDArray.DType
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUES_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUES_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUES_FIELD_NUMBER: _ClassVar[int]
    INT32_VALUES_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUES_FIELD_NUMBER: _ClassVar[int]
    UINT32_VALUES_FIELD_NUMBER: _ClassVar[int]
    UINT64_VALUES_FIELD_NUMBER: _ClassVar[int]
    dtype: NDArray.DType
    shape: _containers.RepeatedScalarFieldContainer[int]
    string_values: _containers.RepeatedScalarFieldContainer[str]
    float_values: _containers.RepeatedScalarFieldContainer[float]
    double_values: _containers.RepeatedScalarFieldContainer[float]
    bool_values: _containers.RepeatedScalarFieldContainer[bool]
    int32_values: _containers.RepeatedScalarFieldContainer[int]
    int64_values: _containers.RepeatedScalarFieldContainer[int]
    uint32_values: _containers.RepeatedScalarFieldContainer[int]
    uint64_values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, dtype: _Optional[_Union[NDArray.DType, str]] = ..., shape: _Optional[_Iterable[int]] = ..., string_values: _Optional[_Iterable[str]] = ..., float_values: _Optional[_Iterable[float]] = ..., double_values: _Optional[_Iterable[float]] = ..., bool_values: _Optional[_Iterable[bool]] = ..., int32_values: _Optional[_Iterable[int]] = ..., int64_values: _Optional[_Iterable[int]] = ..., uint32_values: _Optional[_Iterable[int]] = ..., uint64_values: _Optional[_Iterable[int]] = ...) -> None: ...

class BentoService(_service.service): ...

class BentoService_Stub(BentoService): ...
