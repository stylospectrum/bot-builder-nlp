import random
import grpc
import redis
import json

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer, util
from google.protobuf.json_format import MessageToJson
from google.protobuf import struct_pb2 as _struct_pb2

from ..proto.bot_builder_nlp import bot_builder_nlp_pb2_grpc, bot_builder_nlp_pb2
from ..proto.luna import bentoml_service_pb2_grpc, bentoml_service_pb2
from ..proto.bot_builder_story import bot_builder_story_pb2_grpc, bot_builder_story_pb2
from ..proto.bot_builder_entity import (
    bot_builder_entity_pb2_grpc,
    bot_builder_entity_pb2,
)
from ..utils.get_slots import get_slots, get_best_substring
from ..utils.evaluate_expression import evaluate_expression
from ..utils.milvus import get_milvus_collection
from ..utils.reshape_list import reshape_list
from ..utils.get_json_list import get_json_list
from ..utils.find_block_by_id import find_block_by_id
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
        self.sbert = SentenceTransformer("all-mpnet-base-v2")
        self.paraphraser_tokenizer = AutoTokenizer.from_pretrained(
            "humarin/chatgpt_paraphraser_on_T5_base"
        )
        self.paraphraser_model = AutoModelForSeq2SeqLM.from_pretrained(
            "humarin/chatgpt_paraphraser_on_T5_base"
        )
        redis_port = int(settings.REDIS_PORT)
        self.redis = redis.Redis(
            host="localhost", port=redis_port, decode_responses=True
        )

    def get_user_input_block_id(self, user_input: str, user_id: str) -> tuple:
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
        user_intent = intent_response["json"]["intent"]

        if user_intent == "chitchat":
            embeddings = self.sbert.encode([user_input])
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
            output_fields=["story_block_id", "id"],
            expr=f"user_id == '{user_id}'",
            param={
                "metric_type": "COSINE",
                "offset": 0,
            },
        )
        user_input_block_id = ""
        user_input_id = ""

        for hits in search_result:
            for hit in hits:
                if hit.distance > 0.5:
                    user_input_block_id = hit.entity.get("story_block_id")
                    user_input_id = hit.entity.get("id")
                    break

        return user_input_block_id, user_input_id, user_intent

    def rephrase(self, text: str) -> str:
        should_rephrase = random.choice([True, False])

        if should_rephrase:
            input_ids = self.paraphraser_tokenizer(
                f"paraphrase: {text}",
                return_tensors="pt",
                padding="longest",
                max_length=128,
                truncation=True,
            ).input_ids
            outputs = self.paraphraser_model.generate(
                input_ids,
                num_beams=5,
                num_beam_groups=5,
                num_return_sequences=5,
                repetition_penalty=10.0,
                diversity_penalty=3.0,
                no_repeat_ngram_size=2,
                temperature=0.7,
                max_length=128,
            )
            return self.paraphraser_tokenizer.batch_decode(
                outputs, skip_special_tokens=True
            )

        return [text]

    def get_user_inputs(self, story_block_id: str):
        user_inputs_response: bot_builder_story_pb2.GetUserInputsResponse = (
            self.bot_builder_story_stub.GetUserInputs(
                bot_builder_story_pb2.GetUserInputsRequest(
                    story_block_id=story_block_id
                )
            )
        )
        return get_json_list(user_inputs_response.inputs)

    def get_variables(self, user_id: str):
        variables_response: bot_builder_entity_pb2.GetVariablesResponse = (
            self.bot_builder_entity_stub.GetVariables(
                bot_builder_entity_pb2.GetVariablesRequest(user_id=user_id)
            )
        )
        return get_json_list(variables_response.variables)

    def get_bot_responses(self, story_block_id: str):
        bot_responses_response: bot_builder_story_pb2.GetBotResponsesResponse = (
            self.bot_builder_story_stub.GetBotResponses(
                bot_builder_story_pb2.GetBotResponsesRequest(
                    story_block_id=story_block_id
                )
            )
        )
        return get_json_list(bot_responses_response.responses)

    def get_user_input_by_id(self, id: str, story_block_id: str):
        user_inputs = self.get_user_inputs(story_block_id)
        user_input = next(
            (user_input for user_input in user_inputs if user_input.get("id") == id),
            None,
        )

        if user_input:
            return user_input.get("content", "")

        return ""

    def get_luna_slots(self, text: str):
        slots = self.luna_stub.Call(
            bentoml_service_pb2.Request(
                api_name="classify",
                json=_struct_pb2.Value(
                    struct_value=_struct_pb2.Struct(
                        fields={
                            "text": _struct_pb2.Value(string_value=text),
                            "type": _struct_pb2.Value(string_value="slot"),
                        }
                    )
                ),
            )
        )

        slots = json.loads(MessageToJson(slots, preserving_proto_field_name=True))
        return slots["json"]

    def get_filters(self, story_block_ids: list[str]):
        filters_response: bot_builder_story_pb2.GetFiltersResponse = (
            self.bot_builder_story_stub.GetFilters(
                bot_builder_story_pb2.GetFiltersRequest(story_block_ids=story_block_ids)
            )
        )
        return [
            json.loads(MessageToJson(block, preserving_proto_field_name=True))
            for block in filters_response.filters
        ]

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
        bot_responses = self.get_bot_responses(welcome_msg_block.get("id"))

        result = []

        for response in bot_responses:
            if response["type"] == "Text" or response["type"] == "RandomText":
                response["variants"] = self.rephrase(
                    random.choice(response["variants"])
                )

            result.append(response)

        return bot_builder_nlp_pb2.LoadBotStoryResponse(responses=result)

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
            embeddings = self.sbert.encode(
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

            embeddings = reshape_list(
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
        next_bot_response_block = None
        current_bot_response_block = None
        user_input_block = None
        should_save_user_input_block_id = False
        should_reset_chat = False
        is_save_suggested_gallery = False
        user_input_block_id = ""
        user_input_id = ""
        user_intent = ""
        user_input_raw = ""
        luna_slots = {}
        variables = self.get_variables(request.user_id)

        prev_user_input_block_id = self.redis.hget(
            f"bot_story_nlp:{request.user_id}",
            "prev_user_input_block_id",
        )

        suggested_gallery = self.redis.hget(
            f"bot_story_nlp:{request.user_id}",
            "suggested_gallery",
        )

        if prev_user_input_block_id:
            user_input_block_id = prev_user_input_block_id
        else:
            user_input_block_id, user_input_id, user_intent = (
                self.get_user_input_block_id(request.user_input, request.user_id)
            )

        if user_input_id and user_input_block_id:
            user_input_raw = self.get_user_input_by_id(
                user_input_id, user_input_block_id
            )

        if user_intent not in ["ask", "add_to_cart", ""]:
            self.redis.hdel(
                f"bot_story_nlp:{request.user_id}",
                "suggested_gallery",
            )

        if suggested_gallery:
            suggested_gallery = json.loads(suggested_gallery)
            is_save_suggested_gallery = True
        else:
            suggested_gallery = []
            is_save_suggested_gallery = False

        if request.is_button_click or is_save_suggested_gallery:
            bot_story = self.redis.hget(
                f"bot_story_nlp:{request.user_id}",
                "bot_story",
            )
            bot_story = json.loads(json.loads(bot_story))
            user_input_block = find_block_by_id(bot_story, user_input_block_id)
        else:
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

        if is_save_suggested_gallery and "$" in user_input_raw:
            entities = {}
            exprs = [
                expr
                for gallery_item in suggested_gallery
                for button in gallery_item["buttons"]
                for expr in button["exprs"]
            ]

            for expr in exprs:
                for variable in variables:
                    if variable["id"] == expr["variable_id"]:
                        if entities.get(variable["id"]) is None:
                            entities[variable["id"]] = []
                        entities[variable["id"]].append({"name": expr["value"]})

                    if variable.get("entity") is None:
                        variable["is_user"] = True
                        variable["entity"] = {"name": variable["name"], "options": []}
                    variable["entity"]["options"] = entities.get(variable["id"], [])

                    for option in variable["entity"]["options"]:
                        l = get_best_substring(request.user_input, option["name"])

                        for pos in l:
                            self.redis.hset(
                                f"bot_story_nlp:{request.user_id}",
                                variable["name"],
                                request.user_input[pos["start"] : pos["end"] + 1],
                            )

        if user_input_block:
            child_type = user_input_block.get("children")[0]["type"]

            if child_type == "Filter" or is_save_suggested_gallery:
                luna_slots = self.get_luna_slots(request.user_input)

            if child_type == "Filter":
                slots = get_slots(request.user_input, variables)

                for slot in luna_slots.items():
                    slots[slot[0]] = slot[1]

                for variable in variables:
                    if variable["name"] in request.user_input:
                        expr_value = self.redis.hget(
                            f"bot_story_nlp:{request.user_id}",
                            variable["name"],
                        )
                        slots[variable["name"]] = expr_value

                filter_block_ids = [
                    filter_block.get("id")
                    for filter_block in user_input_block.get("children")
                ]
                filters = self.get_filters(filter_block_ids)

                for filter in filters:
                    if evaluate_expression(filter, slots, variables):
                        for filter_block in user_input_block.get("children"):
                            if filter_block.get("id") == filter.get("story_block_id"):
                                next_bot_response_block = filter_block.get("children")[
                                    0
                                ]
                        break

                if next_bot_response_block:
                    self.redis.hdel(
                        f"bot_story_nlp:{request.user_id}",
                        "prev_user_input_block_id",
                    )

                    if next_bot_response_block.get("children"):
                        self.redis.hset(
                            f"bot_story_nlp:{request.user_id}",
                            "current_bot_response_block",
                            json.dumps(next_bot_response_block),
                        )
                    else:
                        should_reset_chat = True

                else:
                    fallback_block = next(
                        (
                            block
                            for block in user_input_block.get("children")
                            if block.get("type") == "Fallback"
                        ),
                        None,
                    )

                    if fallback_block:
                        next_bot_response_block = fallback_block.get("children")[0]

                        if is_save_suggested_gallery:
                            should_save_user_input_block_id = True

            elif child_type == "BotResponse":
                next_bot_response_block = user_input_block.get("children")[0]

                if next_bot_response_block.get("children"):
                    self.redis.hset(
                        f"bot_story_nlp:{request.user_id}",
                        "current_bot_response_block",
                        json.dumps(next_bot_response_block),
                    )
                else:
                    should_reset_chat = True

        if (
            user_input_block is None
            or next_bot_response_block is None
            or should_reset_chat
        ):
            bot_story = self.redis.hget(
                f"bot_story_nlp:{request.user_id}",
                "bot_story",
            )
            bot_story = json.loads(json.loads(bot_story))
            welcome_msg_block = bot_story.get("children")[0]

            if next_bot_response_block is None or user_input_block is None:
                default_fallback_block = bot_story.get("children")[1]
                next_bot_response_block = default_fallback_block.get("children")[0]

            self.redis.hset(
                f"bot_story_nlp:{request.user_id}",
                "current_bot_response_block",
                json.dumps(welcome_msg_block),
            )

        bot_responses = self.get_bot_responses(next_bot_response_block.get("id"))
        result = []

        for response in bot_responses:
            if response["type"] == "Text" or response["type"] == "RandomText":
                variants = []
                for text in response["variants"]:
                    if should_save_user_input_block_id:
                        embeddings1 = self.sbert.encode(text, convert_to_tensor=True)
                        embeddings2 = self.sbert.encode(
                            "Which one?", convert_to_tensor=True
                        )
                        cosine_scores = util.cos_sim(embeddings1, embeddings2)
                        score = cosine_scores.tolist()[0][0]

                        if score > 0.5:
                            self.redis.hset(
                                f"bot_story_nlp:{request.user_id}",
                                "prev_user_input_block_id",
                                user_input_block_id,
                            )

                    for variable in variables:
                        if variable.get("is_system", False) or (
                            len(variable.get("entity", {})) > 0
                            and not variable.get("is_user")
                        ):
                            continue

                        expr_value = self.redis.hget(
                            f"bot_story_nlp:{request.user_id}",
                            variable["name"],
                        )

                        if variable["name"] in text and expr_value:
                            text = text.replace(f"${variable['name']}", expr_value)
                    variants.append(text)
                response["variants"] = self.rephrase(random.choice(variants))

            if response["type"] == "Gallery" and user_intent == "buy":
                self.redis.hset(
                    f"bot_story_nlp:{request.user_id}",
                    "suggested_gallery",
                    json.dumps(response["gallery"]),
                )

            result.append(response)

        return bot_builder_nlp_pb2.LoadBotStoryResponse(responses=result)

    def GetUserInput(self, request, context):
        variables = self.get_variables(request.user_id)
        user_inputs = self.get_user_inputs(request.story_block_id)
        exprs = get_json_list(request.exprs)
        user_input = random.choice(self.get_user_inputs(user_inputs))
        raw = user_input.get("content", "")
        new = raw

        if len(exprs) > 0:
            for expr in exprs:
                variable = next(
                    (var for var in variables if var["id"] == expr["variable_id"]), None
                )

                if variable:
                    self.redis.hset(
                        f"bot_story_nlp:{request.user_id}",
                        variable["name"],
                        expr["value"],
                    )

                    if variable["name"] and expr["value"]:
                        new = new.replace(f"${variable['name']}", expr["value"])

        return bot_builder_nlp_pb2.GetUserInputResponse(new=new, raw=raw)

    def __del__(self):
        if self.luna_channel:
            self.luna_channel.close()

        if self.bot_builder_story_chanel:
            self.bot_builder_story_chanel.close()

        if self.bot_builder_entity_chanel:
            self.bot_builder_entity_chanel.close()
