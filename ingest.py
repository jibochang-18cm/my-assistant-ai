import uuid
import pypdf
import chromadb

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

        chunk_size = 300
        overlap = 50
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]

            documents.append(chunk)
            metadatas.append({"page": page_num + 1, "source": pdf_path})
            # 用 uuid 而不是从 0 计数，避免和知识库里已有文档的 id 冲突
            ids.append(str(uuid.uuid4()))

    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    # 不再删除已有 collection，新讲义是累加进知识库，不会覆盖之前上传的文档
    collection = chroma_client.get_or_create_collection(name="course_materials")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"解析完成！本次新增 {len(documents)} 个片段，知识库现有 {collection.count()} 个片段。")

if __name__ == "__main__":
    process_pdf_and_store("sample.pdf")
