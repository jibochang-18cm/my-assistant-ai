// 后端接口地址统一在这里配置，本地开发用 127.0.0.1，部署时改成服务器地址即可
const BASE_URL = "http://127.0.0.1:8000";

// 前端维护的多轮对话历史数组
let history = [];

// ===== 上传 PDF =====
async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");
    if (!fileInput.files[0]) {
        alert("请先选择文件");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const statusEl = document.getElementById("uploadStatus");
    statusEl.innerText = "解析中，请稍候...";

    try {
        const res = await fetch(`${BASE_URL}/api/upload`, { method: "POST", body: formData });
        const data = await res.json();
        statusEl.innerText = data.message || data.detail;
    } catch (err) {
        statusEl.innerText = "上传失败: " + err.message;
    }
}

// ===== 发送提问 =====
async function askAI() {
    const qInput = document.getElementById("question");
    const q = qInput.value.trim();
    if (!q) return;

    const chatHistory = document.getElementById("chatHistory");

    // 1. 渲染用户的提问消息框
    const userBox = document.createElement("div");
    userBox.className = "message user-msg";
    userBox.innerText = q;
    chatHistory.appendChild(userBox);

    // 2. 创建 AI 回答消息框
    const aiBox = document.createElement("div");
    aiBox.className = "message ai-msg";
    aiBox.innerText = "AI 思考中...";
    chatHistory.appendChild(aiBox);

    qInput.value = ""; // 清空输入框
    chatHistory.scrollTop = chatHistory.scrollHeight; // 滚动到底部

    let rawText = "";

    try {
        // 3. 发送提问并将 history 一并传给后端
        const response = await fetch(`${BASE_URL}/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: q, history: history })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            rawText += chunk;

            // 使用 marked.parse() 实时把 Markdown 转化为漂亮的 HTML 渲染
            aiBox.innerHTML = marked.parse(rawText);
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }

        // 4. 对话完成后，将本次对话记录压入 history 数组
        history.push({ role: "user", content: q });
        history.push({ role: "assistant", content: rawText });

    } catch (err) {
        aiBox.innerText = "发生错误: " + err.message;
    }
}

// ===== 绑定事件（替代 HTML 内联 onclick）=====
document.getElementById("uploadBtn").addEventListener("click", uploadPDF);
document.getElementById("sendBtn").addEventListener("click", askAI);
