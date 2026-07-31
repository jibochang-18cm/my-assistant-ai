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
collection = chroma_client.get_collection(name="course_materials")
def ask_ai_assistant(query: str):
    collection = chroma_client.get_or_create_collection(name="course_materials")
    if collection.count() == 0:
        return "知识库目前是空的，请先在上方上传一份 PDF 课程讲义！",[]
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    
    retrieved_docs = results['documents'][0]
    retrieved_metas = results['metadatas'][0]
    context_str = ""
    sources = []
    for doc, meta in zip(retrieved_docs, retrieved_metas):
        context_str += f"\n--- 来自第{meta['page']}页 ---\n{doc}\n"
        sources.append(f"第{meta['page']}页")
        system_prompt = """你是一位严谨的高校课程助教。请严格根据提供的课程讲义内容回答学生的提问。
        如果讲义中没有提及，请直接诚实回答：“讲义中未找到相关内容”，不要编造答案。"""
        user_prompt = f"【参考讲义片段】:\n{context_str}\n\n【学生提问】: {query}"
        
        response = client.chat.completions.create(
            model ="deepseek-chat",
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_prompt}
            ],
            temperature=0.3
        )
        answer = response.choices[0].message.content
        return answer, sources
    if __name__ == "__main__":
        question ="什么事TCP的三次握手？"
        ans, src =ask_ai_assistant(question)
        print(f"\nAI 回答:\n{ans}\n")
        print(f"参考出处:{src}")