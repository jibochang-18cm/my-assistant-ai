import os
from openai import OpenAI
from dotenv import load_dotenv

from db import get_collection
from embeddings import embedding_function, QUERY_INSTRUCTION
from utils import display_name

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

RETRIEVAL_TOP_K = 5

def _build_retrieval_query(query: str, history: list) -> str:
    """把最近一轮用户提问拼进检索用的 query，这样"详细说说第一项"这种
    指代不明的追问也能带着上一轮的话题去检索，而不是拿一句没有实际内容
    的话去匹配（这句本身几乎检索不到任何东西）"""
    last_user_turns = [msg["content"] for msg in history[-4:] if msg.get("role") == "user"]
    if last_user_turns:
        return last_user_turns[-1] + " " + query
    return query

def ask_ai_assistant_stream(query: str,history: list = []):
    collection = get_collection()
    if collection.count() == 0:
       yield "知识库目前是空的，请先在上方上传一份 PDF 课程讲义！"
       return

    retrieval_query = _build_retrieval_query(query, history)
    # bge 模型对"提问"需要加引导前缀才能发挥最佳检索效果，讲义原文不用加
    query_embedding = embedding_function([QUERY_INSTRUCTION + retrieval_query])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(RETRIEVAL_TOP_K,collection.count())
    )

    retrieved_docs = results['documents'][0]
    retrieved_metas = results['metadatas'][0]
    context_str = ""
    sources = []
    for doc, meta in zip(retrieved_docs, retrieved_metas):
        doc_name = display_name(meta["source"])
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