# 1. 使用轻量级 Python 3.10 基础镜像
FROM python:3.10-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 设置环境变量：防止 Python 生成 .pyc 文件，并让输出实时打印
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. 复制依赖清单并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 复制项目所有代码到镜像中
COPY . .

# 6. 暴露 FastAPI 的默认端口
EXPOSE 8000

# 7. 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]