from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

from .config.settings import settings


def connect_to_milvus():
    host, port = settings.MILVUS_URL.split(':')
    connections.connect(alias="default", host=host, port=int(port))
    print(f"Connected to Milvus on {host}:{port}")


def get_milvus_collection(collection_name='user_input', dim=768):
    if utility.has_collection(collection_name):
        return Collection(collection_name)

    fields = [
        FieldSchema(name='id', dtype=DataType.VARCHAR, description='ids',
                    max_length=500, is_primary=True, auto_id=False),
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR,
                    description='embedding vectors', dim=dim),
        FieldSchema(name='story_block_id', dtype=DataType.VARCHAR, description='story block ids',
                    max_length=500, auto_id=False),
        FieldSchema(name='user_id', dtype=DataType.VARCHAR, description='user id',
                    max_length=500, auto_id=False),
    ]
    schema = CollectionSchema(
        fields=fields, description='retrieve embeddings of the documents')
    collection = Collection(name=collection_name, schema=schema)

    index_params = {
        'metric_type': 'COSINE',
        'index_type': "IVF_FLAT",
        'params': {"nlist": 1536}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    collection.load()

    return collection
