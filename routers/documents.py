import os
from fastapi import APIRouter

from db import get_collection
from utils import display_name

router = APIRouter()


@router.get("/api/documents")
async def list_documents():
    """列出知识库里已有的讲义，按文件名聚合每份讲义的片段数/页数/大小"""
    collection = get_collection()
    if collection.count() == 0:
        return {"documents": []}

    data = collection.get()

    stats = {}
    for meta in data["metadatas"]:
        source = meta["source"]
        entry = stats.setdefault(source, {"chunk_count": 0, "pages": 0})
        entry["chunk_count"] += 1
        entry["pages"] = max(entry["pages"], meta.get("page", 0))

    documents = []
    for source, info in stats.items():
        documents.append({
            "name": display_name(source),
            "chunk_count": info["chunk_count"],
            "pages": info["pages"],
            "size": os.path.getsize(source) if os.path.exists(source) else None,
        })

    documents.sort(key=lambda d: d["name"])
    return {"documents": documents}
