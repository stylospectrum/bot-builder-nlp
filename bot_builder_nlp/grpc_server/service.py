import grpc

from ..proto.bot_builder_nlp import bot_builder_nlp_pb2_grpc, bot_builder_nlp_pb2
from ..proto.luna import bentoml_service_pb2_grpc, bentoml_service_pb2
from ..milvus import get_milvus_collection
from ..config.settings import settings


class BotBuilderNlpServicer(bot_builder_nlp_pb2_grpc.BotBuilderNlpServiceServicer):
    def __init__(self):
        self.channel = grpc.insecure_channel(settings.LUNA_SERVICE_URL)
        self.luna_stub = bentoml_service_pb2_grpc.BentoServiceStub(
            channel=self.channel)
        self.milvus_collection = get_milvus_collection()

    def reshape_list(self, original_list, n: int, m: int):
        if len(original_list) != n * m:
            raise ValueError(
                "The new size does not match the number of elements in the list.")

        reshaped_list: list[float] = []
        for i in range(n):
            row = []
            for j in range(m):
                row.append(original_list[i * m + j])
            reshaped_list.append(row)

        return reshaped_list

    def UpsertEmbedding(self, request, context):
        luna_response: bentoml_service_pb2.Response = self.luna_stub.Call(bentoml_service_pb2.Request(
            api_name='get_embeddings',
            series=bentoml_service_pb2.Series(string_values=[user_input.content for user_input in request.user_inputs])))
        embeddings = self.reshape_list(
            luna_response.ndarray.float_values, luna_response.ndarray.shape[0], luna_response.ndarray.shape[1])
        ids = [user_input.id for user_input in request.user_inputs]
        story_block_ids = [
            user_input.story_block_id for user_input in request.user_inputs]

        self.milvus_collection.upsert([ids, embeddings, story_block_ids])
        self.milvus_collection.flush()

        return bot_builder_nlp_pb2.UpsertEmbeddingResponse(success=True)

    def DeleteEmbedding(self, request, context):
        expr = 'id in [' + \
            ','.join(map(lambda x: '"' + x + '"', request.ids)) + ']'
        self.milvus_collection.delete(expr)
        return bot_builder_nlp_pb2.DeleteEmbeddingResponse(success=True)

    def GetStoryBlockId(self, request, context):
        luna_response: bentoml_service_pb2.Response = self.luna_stub.Call(bentoml_service_pb2.Request(
            api_name='get_embeddings',
            series=bentoml_service_pb2.Series(string_values=[request.user_input, ''])))
        search_result = self.milvus_collection.search(
            data=[list(luna_response.ndarray.float_values)],
            anns_field="embedding",
            limit=1,
            output_fields=['story_block_id'],
            param={"metric_type": "COSINE", "offset": 0, },
        )
        story_block_id = ''

        for hits in search_result:
            for hit in hits:
                if hit.distance > 0.5:
                    story_block_id = hit.entity.get('story_block_id')
                    break

        return bot_builder_nlp_pb2.GetStoryBlockIdResponse(story_block_id=story_block_id)

    def __del__(self):
        if self.channel:
            self.channel.close()
