from rag import _build_retrieval_query


def test_build_retrieval_query_without_history_returns_query_unchanged():
    assert _build_retrieval_query("你好", []) == "你好"


def test_build_retrieval_query_ignores_assistant_only_history():
    history = [{"role": "assistant", "content": "之前的回答"}]
    assert _build_retrieval_query("追问", history) == "追问"


def test_build_retrieval_query_prepends_last_user_turn():
    # "第二天呢" 这种追问单独检索几乎检索不到任何相关内容，需要带上上一轮的话题
    history = [
        {"role": "user", "content": "新加坡项目日程第一天安排是什么"},
        {"role": "assistant", "content": "第一天是..."},
    ]
    result = _build_retrieval_query("第二天呢", history)
    assert result == "新加坡项目日程第一天安排是什么 第二天呢"


def test_build_retrieval_query_uses_most_recent_user_turn_not_the_oldest():
    history = [
        {"role": "user", "content": "第一个问题"},
        {"role": "assistant", "content": "回答一"},
        {"role": "user", "content": "第二个问题"},
        {"role": "assistant", "content": "回答二"},
    ]
    result = _build_retrieval_query("追问", history)
    assert result == "第二个问题 追问"
