from .milvus import connect_to_milvus
from .grpc_server.module import serve_grpc


def main():
    connect_to_milvus()
    serve_grpc()


if __name__ == '__main__':
    main()
