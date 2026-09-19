import re
import uuid
import pypdf

from db import get_collection

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

# 中英文常见的句末标点/换行，作为切分点，尽量不把一句话切成两半
_SENTENCE_END_RE = re.compile(r'(?<=[。！？!?\n])')


def _split_into_sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_END_RE.split(text) if s.strip()]


def _split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """按句子边界把一页文本切成多个 chunk，单句超长时才退化为按字符硬切"""
    sentences = _split_into_sentences(text)
    chunks = []
    current = ""

    for sentence in sentences:
        # 单个句子本身就超过 chunk_size（比如没有标点的大段文字），只能对这一句退化成硬切
        if len(sentence) > chunk_size:
            if current:
                chunks.append(current)
                current = ""
            for i in range(0, len(sentence), chunk_size - overlap):
                chunks.append(sentence[i:i + chunk_size])
            continue

        if current and len(current) + len(sentence) > chunk_size:
            chunks.append(current)
            # 保留当前块末尾一部分文字作为重叠，让下一块开头有上下文
            current = current[-overlap:] if overlap < len(current) else current

        current += sentence

    if current.strip():
        chunks.append(current)

    return chunks


def process_pdf_and_store(pdf_path: str):
    reader = pypdf.PdfReader(pdf_path)
    documents = []
    metadatas = []
    ids = []

    print("正在解析 PDF并切片中...")

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text.strip():
            continue

        for chunk in _split_into_chunks(text):
            documents.append(chunk)
            metadatas.append({"page": page_num + 1, "source": pdf_path})
            # 用 uuid 而不是从 0 计数，避免和知识库里已有文档的 id 冲突
            ids.append(str(uuid.uuid4()))

    # 不再删除已有 collection，新讲义是累加进知识库，不会覆盖之前上传的文档
    collection = get_collection()

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"解析完成！本次新增 {len(documents)} 个片段，知识库现有 {collection.count()} 个片段。")

if __name__ == "__main__":
    process_pdf_and_store("sample.pdf")
