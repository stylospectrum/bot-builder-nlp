import grpc
import logging

from concurrent import futures

from .service import BotBuilderNlpServicer
from ..proto.bot_builder_nlp import bot_builder_nlp_pb2_grpc
from ..config.settings import settings


def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    bot_builder_nlp_pb2_grpc.add_BotBuilderNlpServiceServicer_to_server(
        BotBuilderNlpServicer(), server
    )
    server.add_insecure_port(f"[::]:{settings.PORT}")
    server.start()

    logging.basicConfig(level=logging.INFO)
    logging.info("gRPC server running...")

    server.wait_for_termination()

    return server
