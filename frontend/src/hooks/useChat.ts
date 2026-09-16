"use client";

import { useCallback, useState } from "react";
import { fetchChatStream, type ChatHistoryItem } from "@/lib/api";
import { uiText } from "@/lib/text";
import type { ChatMessage } from "@/types/chat";

let nextId = 0;
function newId(): string {
  nextId += 1;
  return `msg-${nextId}`;
}

// 多轮对话状态 + 发送逻辑，与具体 UI 无关，方便复用/测试
export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isSending, setIsSending] = useState(false);

  const sendMessage = useCallback(
    async (question: string) => {
      const trimmed = question.trim();
      if (!trimmed || isSending) return;

      // 发给后端的历史不包含这一轮，和原来的多轮记忆逻辑保持一致
      const history: ChatHistoryItem[] = messages.map(({ role, content }) => ({
        role,
        content,
      }));

      const userMessage: ChatMessage = { id: newId(), role: "user", content: trimmed };
      const aiMessageId = newId();
      const aiMessage: ChatMessage = {
        id: aiMessageId,
        role: "assistant",
        content: "", // 空字符串触发 ChatMessageItem 里的打字动画占位
      };

      setMessages((prev) => [...prev, userMessage, aiMessage]);
      setIsSending(true);

      let rawText = "";

      try {
        const stream = await fetchChatStream(trimmed, history);
        const reader = stream.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          rawText += decoder.decode(value, { stream: true });
          const chunkText = rawText;
          setMessages((prev) =>
            prev.map((m) => (m.id === aiMessageId ? { ...m, content: chunkText } : m))
          );
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        setMessages((prev) =>
          prev.map((m) =>
            m.id === aiMessageId ? { ...m, content: uiText.chat.errorPrefix + message } : m
          )
        );
      } finally {
        setIsSending(false);
      }
    },
    [messages, isSending]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return { messages, isSending, sendMessage, clearMessages };
}
