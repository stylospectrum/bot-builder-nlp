# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bot_builder_entity.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x18\x62ot_builder_entity.proto\x12\x1a\x62ot_builder_entity.service"%\n\x12GetEntitiesRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t"K\n\x13GetEntitiesResponse\x12\x34\n\x08\x65ntities\x18\x01 \x03(\x0b\x32".bot_builder_entity.service.Entity"W\n\x06\x45ntity\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x33\n\x07options\x18\x03 \x03(\x0b\x32".bot_builder_entity.service.Option"M\n\x06Option\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x35\n\x08synonyms\x18\x02 \x03(\x0b\x32#.bot_builder_entity.service.Synonym"\x17\n\x07Synonym\x12\x0c\n\x04name\x18\x01 \x01(\t2\x88\x01\n\x16\x42otBuilderStoryService\x12n\n\x0bGetEntities\x12..bot_builder_entity.service.GetEntitiesRequest\x1a/.bot_builder_entity.service.GetEntitiesResponseb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "bot_builder_entity_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_GETENTITIESREQUEST"]._serialized_start = 56
    _globals["_GETENTITIESREQUEST"]._serialized_end = 93
    _globals["_GETENTITIESRESPONSE"]._serialized_start = 95
    _globals["_GETENTITIESRESPONSE"]._serialized_end = 170
    _globals["_ENTITY"]._serialized_start = 172
    _globals["_ENTITY"]._serialized_end = 259
    _globals["_OPTION"]._serialized_start = 261
    _globals["_OPTION"]._serialized_end = 338
    _globals["_SYNONYM"]._serialized_start = 340
    _globals["_SYNONYM"]._serialized_end = 363
    _globals["_BOTBUILDERSTORYSERVICE"]._serialized_start = 366
    _globals["_BOTBUILDERSTORYSERVICE"]._serialized_end = 502
# @@protoc_insertion_point(module_scope)
