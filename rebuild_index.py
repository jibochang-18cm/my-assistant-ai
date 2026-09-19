"""
重建向量知识库。

换了 embedding 模型或者调整了切块策略之后，chroma_db 里已有的向量就和
新代码不兼容了（新旧向量不在同一个语义空间里，检索会不准）。这个脚本会
清空旧的知识库，然后用本地已有的 uploads_*.pdf 原始文件重新解析入库，
不用再一个个手动通过网页重新上传。
"""
import glob

from db import _chroma_client, COLLECTION_NAME
from ingest import process_pdf_and_store

try:
    _chroma_client.delete_collection(COLLECTION_NAME)
    print("已清空旧的知识库")
except Exception:
    print("知识库原本就是空的，直接开始重建")

pdf_files = sorted(glob.glob("./uploads_*.pdf"))

if not pdf_files:
    print("没有找到 uploads_*.pdf 文件，无法重建")
else:
    for pdf_path in pdf_files:
        print(f"\n正在重新处理 {pdf_path} ...")
        process_pdf_and_store(pdf_path)
    print("\n重建完成！")
