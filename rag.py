import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")

def _display_name(source_path: str) -> str:
    """把存储的文件路径变成人类可读的讲义名，去掉 uploads_ 前缀"""
    name = os.path.basename(source_path)
    if name.startswith("uploads_"):
        name = name[len("uploads_"):]
    return name

def ask_ai_assistant_stream(query: str,history: list = []):
    collection = chroma_client.get_or_create_collection(name="course_materials")
    if collection.count() == 0:
       yield "知识库目前是空的，请先在上方上传一份 PDF 课程讲义！"
       return

    results = collection.query(
        query_texts=[query],
        n_results=min(3,collection.count())
    )

    retrieved_docs = results['documents'][0]
    retrieved_metas = results['metadatas'][0]
    context_str = ""
    sources = []
    for doc, meta in zip(retrieved_docs, retrieved_metas):
        doc_name = _display_name(meta["source"])
        context_str += f"\n--- 来自《{doc_name}》第{meta['page']}页 ---\n{doc}\n"
        sources.append(f"《{doc_name}》第{meta['page']}页")

    system_prompt = f"""你是一位严谨的高校课程助教。请严格根据提供的课程讲义内容回答学生的提问。
        如果讲义中没有提及，请直接诚实回答：”讲义中未找到相关内容”，不要编造答案。

        【参考讲义片段】 :
        {context_str}"""
        
    messages =[{"role":"system","content":system_prompt}]
    
    for msg in history[-6:]:
        messages.append({"role":msg["role"],"content":msg["content"]})
        
    messages.append({"role":"user","content":query})
        
    response = client.chat.completions.create(
            model ="deepseek-chat",
            messages=messages,
            temperature=0.3,
            stream=True
        )
    for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    if sources:
        source_str = f"\n\n【参考出处】：{'、'.join(sorted(set(sources)))}"
        yield source_str