// 集中管理界面上的固定文案，改文案只需要改这一个文件
export const uiText = {
  pageTitle: "🎓 高校课程 AI 助教 (多轮记忆 & Markdown)",
  subtitle: "上传课程讲义，AI 结合内容为你答疑，支持多轮追问",

  meta: {
    title: "AI 课程助教",
    description: "高校课程 AI 助教 - 多轮对话与 Markdown 渲染",
  },

  upload: {
    heading: "1. 上传课程讲义 (PDF)",
    uploadButton: "上传解析",
    noFileAlert: "请先选择文件",
    uploading: "解析中，请稍候...",
    uploadFailedPrefix: "上传失败: ",
  },

  chat: {
    heading: "2. 在线对话问答",
    clearButton: "清空对话",
    emptyState: "还没有对话，先上传讲义再来问点什么吧～",
    inputPlaceholder:
      "例如：新加坡第三天的行程是什么？（之后可继续追问：请详细说说第一项）",
    sendButton: "发送提问",
    thinkingAriaLabel: "AI 思考中",
    errorPrefix: "发生错误: ",
  },

  api: {
    genericErrorFallback: (status: number) => `服务器返回错误 (${status})`,
    noStreamBody: "响应中没有可读的数据流",
  },
};
