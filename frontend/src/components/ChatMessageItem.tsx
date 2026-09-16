"use client";

import { marked } from "marked";
import DOMPurify from "dompurify";
import { uiText } from "@/lib/text";
import type { ChatMessage } from "@/types/chat";

export function ChatMessageItem({ message }: { message: ChatMessage }) {
  if (message.role === "user") {
    return (
      <div className="message-row user-row">
        <div className="message user-msg">{message.content}</div>
      </div>
    );
  }

  // 流式回复还没收到第一个 chunk 时，content 为空，显示打字动画占位
  if (message.content === "") {
    return (
      <div className="message-row ai-row">
        <div className="avatar" aria-hidden="true">🤖</div>
        <div className="message ai-msg">
          <span className="typing-dots" aria-label={uiText.chat.thinkingAriaLabel}>
            <span />
            <span />
            <span />
          </span>
        </div>
      </div>
    );
  }

  // marked.parse 在不使用异步扩展时总是同步返回 string；DOMPurify 防止讲义/模型输出里混入的脚本被执行
  const html = DOMPurify.sanitize(marked.parse(message.content) as string);

  return (
    <div className="message-row ai-row">
      <div className="avatar" aria-hidden="true">🤖</div>
      <div className="message ai-msg" dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
}
