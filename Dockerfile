# 使用官方 Python 3.12 镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖和 FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建输入输出目录
RUN mkdir -p /app/input /app/output /app/temp

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONIOENCODING=utf-8

# 创建一个启动脚本
RUN echo '#!/bin/bash\n\
    echo "=== 音乐处理工具容器已启动 ==="\n\
    echo "可用功能:"\n\
    echo "1. FLAC 分割: python flac_splitter.py"\n\
    echo "2. M4S 转 MP3: python m4s_to_mp3_ffmpeg.py"\n\
    echo "3. M4S 转换 (alternative): python convert_m4s.py"\n\
    echo ""\n\
    echo "输入目录: /app/input"\n\
    echo "输出目录: /app/output"\n\
    echo "临时目录: /app/temp"\n\
    echo ""\n\
    echo "使用方法:"\n\
    echo "  将文件放入 input 目录，运行相应的脚本"\n\
    echo "  处理结果将保存在 output 目录"\n\
    echo ""\n\
    exec "$@"' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# 暴露工作目录
VOLUME ["/app/input", "/app/output", "/app/temp"]

# 设置启动脚本
ENTRYPOINT ["/app/entrypoint.sh"]

# 默认命令为 bash，以便用户可以交互式使用
CMD ["/bin/bash"]
