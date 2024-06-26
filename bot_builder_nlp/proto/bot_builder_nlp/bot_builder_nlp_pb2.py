# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bot_builder_nlp.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x62ot_builder_nlp.proto\x12\x17\x62ot_builder_nlp.service\"\x98\x01\n\x13GetUserInputRequest\x12\x19\n\x11\x62ot_response_type\x18\x01 \x01(\t\x12\x16\n\x0estory_block_id\x18\x02 \x01(\t\x12\x0f\n\x07user_id\x18\x03 \x01(\t\x12=\n\x05\x65xprs\x18\x04 \x03(\x0b\x32..bot_builder_nlp.service.BotResponseButtonExpr\"0\n\x14GetUserInputResponse\x12\x0b\n\x03raw\x18\x01 \x01(\t\x12\x0b\n\x03new\x18\x02 \x01(\t\";\n\x15\x42otResponseButtonExpr\x12\x13\n\x0bvariable_id\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"&\n\x13LoadBotStoryRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"O\n\x14LoadBotStoryResponse\x12\x37\n\tresponses\x18\x01 \x03(\x0b\x32$.bot_builder_nlp.service.BotResponse\"V\n\x16GetBotResponsesRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x12\n\nuser_input\x18\x02 \x01(\t\x12\x17\n\x0fis_button_click\x18\x03 \x01(\x08\"R\n\x17GetBotResponsesResponse\x12\x37\n\tresponses\x18\x01 \x03(\x0b\x32$.bot_builder_nlp.service.BotResponse\"r\n\x11\x42otResponseButton\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\x12\r\n\x05go_to\x18\x02 \x01(\t\x12=\n\x05\x65xprs\x18\x03 \x03(\x0b\x32..bot_builder_nlp.service.BotResponseButtonExpr\"\x8a\x01\n\x16\x42otResponseGalleryItem\x12\x0f\n\x07img_url\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12;\n\x07\x62uttons\x18\x04 \x03(\x0b\x32*.bot_builder_nlp.service.BotResponseButton\"\xbd\x01\n\x0b\x42otResponse\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x10\n\x08variants\x18\x02 \x03(\t\x12\x0f\n\x07img_url\x18\x03 \x01(\t\x12;\n\x07\x62uttons\x18\x04 \x03(\x0b\x32*.bot_builder_nlp.service.BotResponseButton\x12@\n\x07gallery\x18\x05 \x03(\x0b\x32/.bot_builder_nlp.service.BotResponseGalleryItem\"@\n\tUserInput\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x16\n\x0estory_block_id\x18\x03 \x01(\t\"b\n\x16UpsertEmbeddingRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x37\n\x0buser_inputs\x18\x02 \x03(\x0b\x32\".bot_builder_nlp.service.UserInput\"*\n\x17UpsertEmbeddingResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"%\n\x16\x44\x65leteEmbeddingRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"*\n\x17\x44\x65leteEmbeddingResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xd2\x04\n\x14\x42otBuilderNlpService\x12k\n\x0cLoadBotStory\x12,.bot_builder_nlp.service.LoadBotStoryRequest\x1a-.bot_builder_nlp.service.LoadBotStoryResponse\x12t\n\x0fGetBotResponses\x12/.bot_builder_nlp.service.GetBotResponsesRequest\x1a\x30.bot_builder_nlp.service.GetBotResponsesResponse\x12t\n\x0fUpsertEmbedding\x12/.bot_builder_nlp.service.UpsertEmbeddingRequest\x1a\x30.bot_builder_nlp.service.UpsertEmbeddingResponse\x12t\n\x0f\x44\x65leteEmbedding\x12/.bot_builder_nlp.service.DeleteEmbeddingRequest\x1a\x30.bot_builder_nlp.service.DeleteEmbeddingResponse\x12k\n\x0cGetUserInput\x12,.bot_builder_nlp.service.GetUserInputRequest\x1a-.bot_builder_nlp.service.GetUserInputResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bot_builder_nlp_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_GETUSERINPUTREQUEST']._serialized_start=51
  _globals['_GETUSERINPUTREQUEST']._serialized_end=203
  _globals['_GETUSERINPUTRESPONSE']._serialized_start=205
  _globals['_GETUSERINPUTRESPONSE']._serialized_end=253
  _globals['_BOTRESPONSEBUTTONEXPR']._serialized_start=255
  _globals['_BOTRESPONSEBUTTONEXPR']._serialized_end=314
  _globals['_LOADBOTSTORYREQUEST']._serialized_start=316
  _globals['_LOADBOTSTORYREQUEST']._serialized_end=354
  _globals['_LOADBOTSTORYRESPONSE']._serialized_start=356
  _globals['_LOADBOTSTORYRESPONSE']._serialized_end=435
  _globals['_GETBOTRESPONSESREQUEST']._serialized_start=437
  _globals['_GETBOTRESPONSESREQUEST']._serialized_end=523
  _globals['_GETBOTRESPONSESRESPONSE']._serialized_start=525
  _globals['_GETBOTRESPONSESRESPONSE']._serialized_end=607
  _globals['_BOTRESPONSEBUTTON']._serialized_start=609
  _globals['_BOTRESPONSEBUTTON']._serialized_end=723
  _globals['_BOTRESPONSEGALLERYITEM']._serialized_start=726
  _globals['_BOTRESPONSEGALLERYITEM']._serialized_end=864
  _globals['_BOTRESPONSE']._serialized_start=867
  _globals['_BOTRESPONSE']._serialized_end=1056
  _globals['_USERINPUT']._serialized_start=1058
  _globals['_USERINPUT']._serialized_end=1122
  _globals['_UPSERTEMBEDDINGREQUEST']._serialized_start=1124
  _globals['_UPSERTEMBEDDINGREQUEST']._serialized_end=1222
  _globals['_UPSERTEMBEDDINGRESPONSE']._serialized_start=1224
  _globals['_UPSERTEMBEDDINGRESPONSE']._serialized_end=1266
  _globals['_DELETEEMBEDDINGREQUEST']._serialized_start=1268
  _globals['_DELETEEMBEDDINGREQUEST']._serialized_end=1305
  _globals['_DELETEEMBEDDINGRESPONSE']._serialized_start=1307
  _globals['_DELETEEMBEDDINGRESPONSE']._serialized_end=1349
  _globals['_BOTBUILDERNLPSERVICE']._serialized_start=1352
  _globals['_BOTBUILDERNLPSERVICE']._serialized_end=1946
# @@protoc_insertion_point(module_scope)
