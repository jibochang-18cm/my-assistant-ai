import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from ingest import process_pdf_and_store

router = APIRouter()

MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB，讲义 PDF 一般用不到这么大
UPLOAD_CHUNK_SIZE = 1024 * 1024  # 每次读 1MB，避免大文件一次性占满内存


async def _save_upload_file(file: UploadFile) -> str:
    """把上传的文件安全地写到磁盘，返回保存路径；超出大小限制会清理并抛 HTTPException"""
    # basename 去掉文件名里的路径部分，防止 ../ 或绝对路径写到 uploads 目录之外
    safe_filename = os.path.basename(file.filename)
    save_path = f"./uploads_{safe_filename}"

    total_size = 0
    too_large = False
    with open(save_path, "wb") as buffer:
        while True:
            chunk = await file.read(UPLOAD_CHUNK_SIZE)
            if not chunk:
                break
            total_size += len(chunk)
            if total_size > MAX_UPLOAD_SIZE:
                too_large = True
                break
            buffer.write(chunk)

    if too_large:
        os.remove(save_path)
        raise HTTPException(
            status_code=413,
            detail=f"文件过大，最大支持 {MAX_UPLOAD_SIZE // (1024 * 1024)}MB"
        )

    return save_path


@router.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="只能上传 PDF 文件")

    save_path = await _save_upload_file(file)

    try:
        process_pdf_and_store(save_path)
        return {"status": "success", "message": f"文件 {file.filename}已成功解析并倒入知识库！"}
    except Exception as e:
        # 解析失败就不该在磁盘上留下这个文件，避免出现"文件存在但没有真正入库"的不一致状态
        if os.path.exists(save_path):
            os.remove(save_path)
        raise HTTPException(status_code=500, detail=str(e))
