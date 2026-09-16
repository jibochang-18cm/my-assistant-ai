from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import upload, chat

app = FastAPI(title="高校课程 AI 助教 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(upload.router)
app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
