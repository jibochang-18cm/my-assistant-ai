import chromadb

from embeddings import embedding_function

_chroma_client = chromadb.PersistentClient(path="./chroma_db")

COLLECTION_NAME = "course_materials"


def get_collection():
    """ingest.py（写入）、rag.py（查询）、routers/documents.py（列表）都从这里拿同一个 collection"""
    return _chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )
