import grpc
import redis
import json

from sentence_transformers import SentenceTransformer
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.json_format import MessageToJson
from google.protobuf import struct_pb2 as _struct_pb2

from ..proto.bot_builder_nlp import bot_builder_nlp_pb2_grpc, bot_builder_nlp_pb2
from ..proto.luna import bentoml_service_pb2_grpc, bentoml_service_pb2
from ..proto.bot_builder_story import bot_builder_story_pb2_grpc, bot_builder_story_pb2
from ..proto.bot_builder_entity import (
    bot_builder_entity_pb2_grpc,
    bot_builder_entity_pb2,
)
from ..utils.get_slots import get_slots
from ..utils.evaluate_expression import evaluate_expression
from ..utils.milvus import get_milvus_collection
from ..config.settings import settings


class BotBuilderNlpServicer(bot_builder_nlp_pb2_grpc.BotBuilderNlpServiceServicer):
    def __init__(self):
        self.luna_channel = grpc.insecure_channel(settings.LUNA_SERVICE_URL)
        self.luna_stub = bentoml_service_pb2_grpc.BentoServiceStub(
            channel=self.luna_channel
        )

        self.bot_builder_story_chanel = grpc.insecure_channel(
            settings.BOT_BUILDER_STORY_SERVICE_URL
        )
        self.bot_builder_story_stub = (
            bot_builder_story_pb2_grpc.BotBuilderStoryServiceStub(
                channel=self.bot_builder_story_chanel
            )
        )

        self.bot_builder_entity_chanel = grpc.insecure_channel(
            settings.BOT_BUILDER_ENTITY_SERVICE_URL
        )
        self.bot_builder_entity_stub = (
            bot_builder_entity_pb2_grpc.BotBuilderStoryServiceStub(
                channel=self.bot_builder_entity_chanel
            )
        )

        self.milvus_collection = get_milvus_collection()
        self.embedding = SentenceTransformer("all-mpnet-base-v2")

        redis_port = int(settings.REDIS_PORT)
        self.redis = redis.Redis(
            host="localhost", port=redis_port, decode_responses=True
        )

    def reshape_list(self, original_list, n: int, m: int):
        if len(original_list) != n * m:
            raise ValueError(
                "The new size does not match the number of elements in the list."
            )

        reshaped_list: list[float] = []
        for i in range(n):
            row = []
            for j in range(m):
                row.append(original_list[i * m + j])
            reshaped_list.append(row)

        return reshaped_list

    def get_user_input_block_id(self, user_input: str, user_id: str) -> str:
        intent_response: bentoml_service_pb2.Response = self.luna_stub.Call(
            bentoml_service_pb2.Request(
                api_name="classify",
                json=_struct_pb2.Value(
                    struct_value=_struct_pb2.Struct(
                        fields={
                            "text": _struct_pb2.Value(string_value=user_input),
                            "type": _struct_pb2.Value(string_value="intent"),
                        }
                    )
                ),
            )
        )
        intent_response = json.loads(
            MessageToJson(intent_response, preserving_proto_field_name=True)
        )

        if intent_response["json"]["intent"] == "chitchat":
            embeddings = self.embedding.encode([user_input])
            embeddings = [x.tolist() for x in embeddings]
        else:
            luna_embedding: bentoml_service_pb2.Response = self.luna_stub.Call(
                bentoml_service_pb2.Request(
                    api_name="get_embeddings",
                    series=bentoml_service_pb2.Series(string_values=[user_input, ""]),
                )
            )
            embeddings = [list(luna_embedding.ndarray.float_values)]

        search_result = self.milvus_collection.search(
            data=embeddings,
            anns_field="embedding",
            limit=1,
            output_fields=["story_block_id"],
            expr=f"user_id == '{user_id}'",
            param={
                "metric_type": "COSINE",
                "offset": 0,
            },
        )
        id: str = ""

        for hits in search_result:
            for hit in hits:
                if hit.distance > 0.5:
                    id = hit.entity.get("story_block_id")
                    break

        return id

    def LoadBotStory(self, request, context):
        self.redis.delete(f"bot_story_nlp:{request.user_id}")

        story_block = self.bot_builder_story_stub.GetStoryBlocks(
            bot_builder_story_pb2.GetStoryBlocksRequest(user_id=request.user_id)
        )
        story_block = MessageToJson(story_block, preserving_proto_field_name=True)
        self.redis.hset(
            f"bot_story_nlp:{request.user_id}", "bot_story", json.dumps(story_block)
        )
        story_block = json.loads(story_block)

        welcome_msg_block = story_block.get("children")[0]
        self.redis.hset(
            f"bot_story_nlp:{request.user_id}",
            "current_bot_response_block",
            json.dumps(welcome_msg_block),
        )
        bot_responses: bot_builder_story_pb2.GetBotResponsesResponse = (
            self.bot_builder_story_stub.GetBotResponses(
                bot_builder_story_pb2.GetBotResponsesRequest(
                    story_block_id=welcome_msg_block.get("id")
                )
            )
        )
        bot_responses = json.loads(
            MessageToJson(bot_responses, preserving_proto_field_name=True)
        )
        return bot_builder_nlp_pb2.LoadBotStoryResponse(
            responses=bot_responses.get("responses")
        )

    def UpsertEmbedding(self, request, context):
        embeddings = []
        intent_response = self.luna_stub.Call(
            bentoml_service_pb2.Request(
                api_name="classify",
                json=_struct_pb2.Value(
                    struct_value=_struct_pb2.Struct(
                        fields={
                            "text": _struct_pb2.Value(
                                string_value=request.user_inputs[0].content
                            ),
                            "type": _struct_pb2.Value(string_value="intent"),
                        }
                    )
                ),
            )
        )
        intent_response = json.loads(
            MessageToJson(intent_response, preserving_proto_field_name=True)
        )

        if intent_response["json"]["intent"] == "chitchat":
            embeddings = self.embedding.encode(
                [user_input.content for user_input in request.user_inputs]
            )
            embeddings = [x.tolist() for x in embeddings]
        else:
            if len(request.user_inputs) == 1:
                string_values = [request.user_inputs[0].content, ""]
            else:
                string_values = [
                    user_input.content for user_input in request.user_inputs
                ]

            luna_embedding: bentoml_service_pb2.Response = self.luna_stub.Call(
                bentoml_service_pb2.Request(
                    api_name="get_embeddings",
                    series=bentoml_service_pb2.Series(string_values=string_values),
                )
            )

            embeddings = self.reshape_list(
                luna_embedding.ndarray.float_values,
                luna_embedding.ndarray.shape[0],
                luna_embedding.ndarray.shape[1],
            )

        ids = [user_input.id for user_input in request.user_inputs]
        story_block_ids = [
            user_input.story_block_id for user_input in request.user_inputs
        ]
        user_ids = [request.user_id] * len(ids)

        self.milvus_collection.upsert([ids, embeddings, story_block_ids, user_ids])
        self.milvus_collection.flush()

        return bot_builder_nlp_pb2.UpsertEmbeddingResponse(success=True)

    def DeleteEmbedding(self, request, context):
        expr = "id in [" + ",".join(map(lambda x: '"' + x + '"', request.ids)) + "]"
        self.milvus_collection.delete(expr)

        return bot_builder_nlp_pb2.DeleteEmbeddingResponse(success=True)

    def GetBotResponses(self, request, context):
        result = []
        user_input_block_id = self.get_user_input_block_id(
            request.user_input, request.user_id
        )
        current_bot_response_block = self.redis.hget(
            f"bot_story_nlp:{request.user_id}",
            "current_bot_response_block",
        )
        current_bot_response_block = json.loads(current_bot_response_block)
        user_input_block = next(
            (
                block
                for block in current_bot_response_block.get("children", [])
                if block.get("id") == user_input_block_id
            ),
            None,
        )
        bot_response_block = None

        if user_input_block:
            if user_input_block.get("children")[0]["type"] == "Filter":
                entities_response: bot_builder_entity_pb2.GetEntitiesResponse = (
                    self.bot_builder_entity_stub.GetEntities(
                        bot_builder_entity_pb2.GetEntitiesRequest(
                            user_id=request.user_id
                        )
                    )
                )
                entities: list[bot_builder_entity_pb2.Entity] = [
                    json.loads(MessageToJson(entity, preserving_proto_field_name=True))
                    for entity in entities_response.entities
                ]
                slots = get_slots(request.user_input, entities)
                luna_slots = self.luna_stub.Call(
                    bentoml_service_pb2.Request(
                        api_name="classify",
                        json=_struct_pb2.Value(
                            struct_value=_struct_pb2.Struct(
                                fields={
                                    "text": _struct_pb2.Value(
                                        string_value=request.user_input
                                    ),
                                    "type": _struct_pb2.Value(string_value="slot"),
                                }
                            )
                        ),
                    )
                )

                luna_slots = json.loads(
                    MessageToJson(luna_slots, preserving_proto_field_name=True)
                )
                luna_slots = luna_slots["json"]

                for slot in luna_slots.items():
                    slots[slot[0]] = slot[1]

                filter_block_ids = [
                    filter_block.get("id")
                    for filter_block in user_input_block.get("children")
                ]
                filters_response: bot_builder_story_pb2.GetFiltersResponse = (
                    self.bot_builder_story_stub.GetFilters(
                        bot_builder_story_pb2.GetFiltersRequest(
                            story_block_ids=filter_block_ids
                        )
                    )
                )
                filters = [
                    json.loads(MessageToJson(block, preserving_proto_field_name=True))
                    for block in filters_response.filters
                ]

                for filter in filters:
                    if evaluate_expression(filter, slots, entities):
                        for filter_block in user_input_block.get("children"):
                            if filter_block.get("id") == filter.get("story_block_id"):
                                bot_response_block = filter_block.get("children")[0]
                        break

                if bot_response_block is None:
                    fallback_block = next(
                        (
                            block
                            for block in user_input_block.get("children")
                            if block.get("type") == "Fallback"
                        ),
                        None,
                    )

                    if fallback_block:
                        bot_response_block = fallback_block.get("children")[0]
                else:
                    self.redis.hset(
                        f"bot_story_nlp:{request.user_id}",
                        "current_bot_response_block",
                        json.dumps(bot_response_block),
                    )

            elif user_input_block.get("children")[0]["type"] == "BotResponse":
                bot_response_block = user_input_block.get("children")[0]
                self.redis.hset(
                    f"bot_story_nlp:{request.user_id}",
                    "current_bot_response_block",
                    json.dumps(bot_response_block),
                )

        if user_input_block is None or bot_response_block is None:
            bot_story = self.redis.hget(
                f"bot_story_nlp:{request.user_id}",
                "bot_story",
            )
            bot_story = json.loads(json.loads(bot_story))
            welcome_msg_block = bot_story.get("children")[0]
            default_fallback_block = bot_story.get("children")[1]
            bot_response_block = default_fallback_block.get("children")[0]

            self.redis.hset(
                f"bot_story_nlp:{request.user_id}",
                "current_bot_response_block",
                json.dumps(welcome_msg_block),
            )

        bot_responses: bot_builder_story_pb2.GetBotResponsesResponse = (
            self.bot_builder_story_stub.GetBotResponses(
                bot_builder_story_pb2.GetBotResponsesRequest(
                    story_block_id=bot_response_block.get("id")
                )
            )
        )
        result = json.loads(
            MessageToJson(
                bot_responses,
                preserving_proto_field_name=True,
            )
        )
        result = result.get("responses")

        return bot_builder_nlp_pb2.LoadBotStoryResponse(responses=result)

    def __del__(self):
        if self.luna_channel:
            self.luna_channel.close()

        if self.bot_builder_story_chanel:
            self.bot_builder_story_chanel.close()

        if self.bot_builder_entity_chanel:
            self.bot_builder_entity_chanel.close()
