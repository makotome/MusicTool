# Docker 部署使用说明

## 🐳 Docker 部署指南

本项目支持通过 Docker 容器化部署，方便在任何支持 Docker 的环境中运行音乐处理工具。

### 📋 前置要求

- Docker
- Docker Compose (可选，推荐)

### 🚀 快速开始

#### 方法一：使用 Docker Compose (推荐)

1. **构建并启动容器**
```bash
docker-compose up -d --build
```

2. **进入容器**
```bash
docker-compose exec music-tool bash
```

3. **使用工具**
```bash
# 在容器内运行
python flac_splitter.py      # FLAC 分割工具
python m4s_to_mp3_ffmpeg.py  # M4S 转 MP3 工具
```

4. **停止容器**
```bash
docker-compose down
```

#### 方法二：使用 Docker 命令

1. **构建镜像**
```bash
docker build -t music-tool .
```

2. **运行容器**
```bash
docker run -it \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/temp:/app/temp \
  -v $(pwd)/m4s:/app/m4s \
  -v $(pwd)/donglihuoche1:/app/donglihuoche1 \
  --name music-tool-container \
  music-tool
```

### 📁 目录结构

容器会自动创建以下目录挂载点：

```
宿主机目录          →  容器内目录
./input            →  /app/input       # 输入文件
./output           →  /app/output      # 输出文件
./temp             →  /app/temp        # 临时文件
./m4s              →  /app/m4s         # M4S 源文件
./donglihuoche1    →  /app/donglihuoche1  # FLAC 源文件
```

### 💡 使用示例

#### FLAC 文件分割

1. 将 FLAC 文件和对应的 CUE 文件放入 `./input` 目录
2. 进入容器执行分割命令
3. 分割后的文件将保存在 `./output` 目录

```bash
# 进入容器
docker-compose exec music-tool bash

# 执行分割（假设文件在 input 目录）
cd /app/input
python /app/flac_splitter.py
```

#### M4S 转 MP3

1. 将 M4S 文件放入 `./m4s` 目录
2. 进入容器执行转换命令
3. 转换后的 MP3 文件将保存在 `./mp3_output` 目录

```bash
# 进入容器
docker-compose exec music-tool bash

# 执行转换
python m4s_to_mp3_ffmpeg.py
```

### 🔧 高级配置

#### 自定义目录挂载

如果你的音频文件在其他位置，可以修改 `docker-compose.yml` 文件的 volumes 配置：

```yaml
volumes:
  - /path/to/your/music:/app/music
  - /path/to/output:/app/output
```

#### 持久化配置

容器重启后数据会保留在挂载的目录中，包括：
- 转换后的音频文件
- 日志文件
- 临时文件

### 🐛 故障排除

#### 常见问题

1. **权限问题**
   ```bash
   # 确保目录有正确的权限
   chmod 755 ./input ./output ./temp
   ```

2. **中文编码问题**
   - 容器已配置 UTF-8 编码
   - 确保输入文件名使用 UTF-8 编码

3. **FFmpeg 相关错误**
   - 容器已预装 FFmpeg
   - 如有问题可以重新构建镜像

#### 查看日志

```bash
# 查看容器日志
docker-compose logs music-tool

# 实时查看日志
docker-compose logs -f music-tool
```

### 🔄 更新和维护

#### 更新代码后重新构建

```bash
docker-compose down
docker-compose up -d --build
```

#### 清理容器和镜像

```bash
# 停止并删除容器
docker-compose down --volumes

# 删除镜像
docker rmi music-tool
```

### 📝 注意事项

1. **文件路径**：在容器内使用绝对路径 `/app/...`
2. **性能**：大文件处理可能需要更多内存，可以通过 Docker 配置调整
3. **存储空间**：确保宿主机有足够的存储空间用于音频文件
4. **网络**：容器默认使用桥接网络，无需额外配置

### 🎯 生产环境部署

如需在生产环境部署，建议：

1. 使用固定版本的基础镜像
2. 配置健康检查
3. 设置资源限制
4. 配置日志轮转
5. 使用专用的数据卷

示例生产配置：

```yaml
version: '3.8'
services:
  music-tool:
    build: .
    restart: unless-stopped
    mem_limit: 2g
    cpus: 1.0
    volumes:
      - music_data:/app/data
    healthcheck:
      test: ["CMD", "python", "--version"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  music_data:
```
