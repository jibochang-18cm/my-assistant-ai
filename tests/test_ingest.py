from ingest import _split_into_sentences, _split_into_chunks


def test_split_into_sentences_basic():
    text = "这是第一句。这是第二句！这是第三句？"
    assert _split_into_sentences(text) == ["这是第一句。", "这是第二句！", "这是第三句？"]


def test_split_into_sentences_keeps_newline_as_boundary():
    text = "第一行\n第二行\n"
    assert _split_into_sentences(text) == ["第一行\n", "第二行\n"]


def test_split_into_sentences_no_punctuation_is_one_sentence():
    text = "只有一句话没有标点"
    assert _split_into_sentences(text) == ["只有一句话没有标点"]


def test_split_into_chunks_empty_text():
    assert _split_into_chunks("") == []


def test_split_into_chunks_merges_short_sentences_into_one_chunk():
    # 两句加起来远没超过 chunk_size，应该被合并到同一个 chunk，而不是各占一块
    text = "短句一。" + "短句二。"
    chunks = _split_into_chunks(text, chunk_size=50, overlap=10)
    assert chunks == [text]


def test_split_into_chunks_never_breaks_a_sentence_in_the_middle():
    # 原来的实现是按字符硬切，会把句子从中间切断；这里验证每个 chunk 的结尾
    # 要么是完整句子的标点，要么是整段文本的末尾——不会停在句子内部的某个字上
    sentences = ["第一句内容比较长一些。", "第二句内容也不短。", "第三句用来把长度堆上去。"]
    text = "".join(sentences)
    chunks = _split_into_chunks(text, chunk_size=20, overlap=5)

    for chunk in chunks:
        stripped = chunk.rstrip()
        assert stripped == "" or stripped[-1] in "。！？!?"


def test_split_into_chunks_respects_chunk_size_limit():
    sentence = "字" * 20 + "。"  # 21 字/句
    text = sentence * 5  # 105 字，5 句
    chunks = _split_into_chunks(text, chunk_size=50, overlap=10)
    assert len(chunks) > 1
    assert all(len(c) <= 50 for c in chunks)


def test_split_into_chunks_falls_back_to_hard_cut_for_unpunctuated_run():
    # 没有任何标点/换行的超长文本（比如没排版的扫描件），必须能兜底按字符硬切，
    # 不能因为找不到句子边界就死循环或者产出超长 chunk
    text = "无标点内容" * 100  # 500 字，没有一个标点
    chunks = _split_into_chunks(text, chunk_size=300, overlap=50)
    assert len(chunks) > 1
    assert all(len(c) <= 300 for c in chunks)
