from chromadb.utils import embedding_functions

# BAAI/bge-small-zh-v1.5：专门针对中文语义检索优化的小模型。
# Chroma 默认的 all-MiniLM-L6-v2 主要面向英文，处理中文课程讲义时
# 语义相似度判断不准，检索效果差——这里统一换成中文模型。
# ingest.py（写入）和 rag.py（查询）必须用同一个 embedding function，
# 否则两边算出来的向量不在同一个空间里，检索会完全不准，所以放在这个
# 公共模块里给两边一起 import。
CHINESE_EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=CHINESE_EMBEDDING_MODEL
)

# bge 系列模型是非对称检索模型：官方建议只给"提问"加这个引导前缀，
# 讲义原文不用加，这样问题和内容的向量会更匹配，检索精度明显更好。
QUERY_INSTRUCTION = "为这个句子生成表示以用于检索相关文章："
