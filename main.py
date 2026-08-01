from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List,Dict,Optional
from pydantic import BaseModel
import shutil
import os
from ingest import process_pdf_and_store
from rag import ask_ai_assistant_stream
app = FastAPI(title="高校课程 AI 助教 API")

class QueryRequest(BaseModel):
    question: str
    history: Optional[List[Dict[str,str]]] = []
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)
    
@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400,detail="只能上传 PDF 文件")
    save_path = f"./uploads_{file.filename}"
    with open(save_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
        
    try:
        process_pdf_and_store(save_path)
        return {"status":"success","message":f"文件 {file.filename}已成功解析并倒入知识库！"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.post("/api/chat")
async def chat(req:QueryRequest):
    """接口 2:向 AI 助教提问"""
    if not req.question.strip():
        raise HTTPException(status_code=400,detail="提问不能为空")
    return StreamingResponse(
        ask_ai_assistant_stream(req.question,req.history),
        media_type="text/event-stream"
    )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)