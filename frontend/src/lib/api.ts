// 网络层：只负责和后端 FastAPI 通信，不涉及任何 DOM / React 状态
import { uiText } from "@/lib/text";

export const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

async function parseErrorMessage(res: Response): Promise<string> {
  const data = await res.json().catch(() => null);
  return data?.detail || uiText.api.genericErrorFallback(res.status);
}

export interface UploadResponse {
  status: string;
  message: string;
}

export async function uploadPdf(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/api/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    throw new Error(await parseErrorMessage(res));
  }
  return res.json();
}

export interface ChatHistoryItem {
  role: "user" | "assistant";
  content: string;
}

// 发起提问，返回可供逐块读取的响应流
export async function fetchChatStream(
  question: string,
  history: ChatHistoryItem[]
): Promise<ReadableStream<Uint8Array>> {
  const res = await fetch(`${BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, history }),
  });
  if (!res.ok) {
    throw new Error(await parseErrorMessage(res));
  }
  if (!res.body) {
    throw new Error(uiText.api.noStreamBody);
  }
  return res.body;
}
