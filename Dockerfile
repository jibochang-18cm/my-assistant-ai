# 1. 使用轻量级 Python 3.10 基础镜像
FROM python:3.10-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 设置环境变量：防止 Python 生成 .pyc 文件，并让输出实时打印
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. 安装系统依赖并升级 SQLite3 到 3.45.3（>=3.35.0）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        ca-certificates && \
    # 下载并编译 SQLite3 3.45.3
    wget https://www.sqlite.org/2024/sqlite-autoconf-3450300.tar.gz && \
    tar xzf sqlite-autoconf-3450300.tar.gz && \
    cd sqlite-autoconf-3450300 && \
    ./configure --prefix=/usr/local --disable-static --enable-shared && \
    make -j$(nproc) && \
    make install && \
    # 更新动态链接库路径
    echo "/usr/local/lib" > /etc/ld.so.conf.d/sqlite3.conf && \
    ldconfig && \
    # 清理临时文件以减小镜像体积
    cd .. && \
    rm -rf sqlite-autoconf-3450300* && \
    apt-get purge -y --auto-remove build-essential wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 5. 复制依赖清单并安装（使用清华源加速）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 6. 复制项目所有代码到镜像中
COPY . .

# 7. 暴露 FastAPI 的默认端口
EXPOSE 8000

# 8. 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
