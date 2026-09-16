"use client";

import { useEffect, useRef, type KeyboardEvent } from "react";
import { useChat } from "@/hooks/useChat";
import { uiText } from "@/lib/text";
import { ChatMessageItem } from "./ChatMessageItem";

export function ChatPanel() {
  const { messages, isSending, sendMessage, clearMessages } = useChat();
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const historyRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (historyRef.current) {
      historyRef.current.scrollTop = historyRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    const textarea = inputRef.current;
    if (!textarea) return;
    const question = textarea.value.trim();
    if (!question) return;

    textarea.value = "";
    void sendMessage(question).then(() => textarea.focus());
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="box">
      <div className="panel-header">
        <h3>{uiText.chat.heading}</h3>
        <button
          className="btn-secondary"
          onClick={clearMessages}
          disabled={isSending || messages.length === 0}
        >
          {uiText.chat.clearButton}
        </button>
      </div>
      <div className="chat-history" ref={historyRef}>
        {messages.length === 0 ? (
          <p className="chat-empty">{uiText.chat.emptyState}</p>
        ) : (
          messages.map((m) => <ChatMessageItem key={m.id} message={m} />)
        )}
      </div>
      <textarea
        ref={inputRef}
        placeholder={uiText.chat.inputPlaceholder}
        onKeyDown={handleKeyDown}
        disabled={isSending}
      />
      <br />
      <br />
      <button onClick={handleSend} disabled={isSending}>
        {uiText.chat.sendButton}
      </button>
    </div>
  );
}
