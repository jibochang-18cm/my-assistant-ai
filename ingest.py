import pypdf
import chromadb
def process_pdf_and_store(pdf_path:str):
    #
    reader = pypdf.PdfReader(pdf_path)
    documents = []
    metadatas = []
    ids = []
    
    print("正在解析 PDF并切片中...")
    doc_id = 0
    
    #
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text.strip():
            continue
        
        chunk_size = 300
        overlap = 50
        for i in range(0,len(text),chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            
            documents.append(chunk)
            metadatas.append({"page":page_num +1,"source":pdf_path})
            ids.append(f"doc_{doc_id}")
            doc_id += 1
            
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        chroma_client.delete_collection("course_materials")
    except:
        pass
    collection = chroma_client.get_or_create_collection(name="course_materials")
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"解析完成！共切分成{len(documents)}个片段，已成功存入本地向量库。")
    
if __name__ == "__main__":
    process_pdf_and_store("sample.pdf")