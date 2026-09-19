import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from routers import upload as upload_module

client = TestClient(app)

TEST_UPLOAD_PATH = "./uploads_pytest_test.pdf"


def _cleanup():
    if os.path.exists(TEST_UPLOAD_PATH):
        os.remove(TEST_UPLOAD_PATH)


def test_upload_rejects_non_pdf_extension():
    response = client.post(
        "/api/upload",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400


def test_upload_sanitizes_path_traversal_filename():
    _cleanup()
    try:
        with patch("routers.upload.process_pdf_and_store") as mock_process:
            response = client.post(
                "/api/upload",
                files={"file": ("../../etc/pytest_test.pdf", b"%PDF-1.4 fake", "application/pdf")},
            )
        assert response.status_code == 200
        # 文件应该落在项目目录里，而不是逃逸到 /etc
        assert os.path.exists(TEST_UPLOAD_PATH)
        assert not os.path.exists("/etc/pytest_test.pdf")
        mock_process.assert_called_once()
    finally:
        _cleanup()


def test_upload_rejects_oversized_file():
    _cleanup()
    original_max = upload_module.MAX_UPLOAD_SIZE
    upload_module.MAX_UPLOAD_SIZE = 10  # 临时调小，不用真的传 50MB 的文件
    try:
        with patch("routers.upload.process_pdf_and_store"):
            response = client.post(
                "/api/upload",
                files={"file": ("pytest_test.pdf", b"x" * 100, "application/pdf")},
            )
        assert response.status_code == 413
        # 超限的文件不应该在磁盘上留下痕迹
        assert not os.path.exists(TEST_UPLOAD_PATH)
    finally:
        upload_module.MAX_UPLOAD_SIZE = original_max
        _cleanup()


def test_upload_cleans_up_file_on_parse_failure():
    _cleanup()
    try:
        with patch("routers.upload.process_pdf_and_store", side_effect=ValueError("boom")):
            response = client.post(
                "/api/upload",
                files={"file": ("pytest_test.pdf", b"%PDF-1.4 fake", "application/pdf")},
            )
        assert response.status_code == 500
        # 客户端只应该看到统一的安全提示，不应该看到 "boom" 这种内部异常细节
        assert "boom" not in response.text
        assert "文件解析失败" in response.json()["detail"]
        assert not os.path.exists(TEST_UPLOAD_PATH)
    finally:
        _cleanup()


def test_upload_success_returns_message():
    _cleanup()
    try:
        with patch("routers.upload.process_pdf_and_store") as mock_process:
            response = client.post(
                "/api/upload",
                files={"file": ("pytest_test.pdf", b"%PDF-1.4 fake", "application/pdf")},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        mock_process.assert_called_once()
    finally:
        _cleanup()
