from utils import display_name


def test_display_name_strips_uploads_prefix():
    assert display_name("./uploads_数据库复习笔记.pdf") == "数据库复习笔记.pdf"


def test_display_name_strips_directory_components():
    assert display_name("/some/other/path/uploads_notes.pdf") == "notes.pdf"


def test_display_name_leaves_name_unchanged_without_prefix():
    assert display_name("./random_file.pdf") == "random_file.pdf"
