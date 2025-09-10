# 使用官方 Python 运行时作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖和 FFmpeg（添加重试机制）
RUN apt-get update && \
    for i in 1 2 3; do \
    apt-get install -y ffmpeg && break || \
    (echo "Install attempt $i failed, retrying..." && sleep 5); \
    done && \
    rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建输入输出目录
RUN mkdir -p /app/input /app/output /app/temp /app/uploads

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONIOENCODING=utf-8
ENV FLASK_APP=web_app.py
ENV FLASK_ENV=production

# 暴露端口
EXPOSE 5000

# 暴露工作目录
VOLUME ["/app/input", "/app/output", "/app/temp", "/app/uploads"]

# 默认启动 Web 界面
CMD ["python", "web_app.py"]
