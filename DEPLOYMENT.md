# MusicTool Docker 部署指南

## 重要说明

### 架构兼容性
- **Mac (Apple Silicon)**: 默认构建 ARM64 架构镜像
- **绿联私有云/Linux服务器**: 需要 AMD64 架构镜像

### 构建不同架构的镜像
```bash
# 构建 AMD64 架构镜像（适用于绿联私有云）
docker build --platform linux/amd64 -t musictool:amd64 .

# 构建 ARM64 架构镜像（适用于 Apple Silicon Mac）
docker build --platform linux/arm64 -t musictool:arm64 .

# 保存镜像
docker save -o musictool-amd64.tar musictool:amd64
docker save -o musictool-arm64.tar musictool:arm64
```

## 方案一：使用 Docker Hub（推荐）

### 1. 本地构建和推送镜像

```bash
# 登录 Docker Hub
docker login

# 构建镜像
docker build -t makotome/musictool:latest .

# 推送到 Docker Hub
docker push makotome/musictool:latest
```

### 2. 在绿联私有云上拉取和运行

```bash
# 上传 musictool-amd64.tar 到绿联私有云后
# 加载镜像
docker load -i musictool-amd64.tar

# 运行容器
docker run -d \
  --name music-tool-web \
  -p 5001:5000 \
  -v /volume1/docker/MusicTool/input:/app/input \
  -v /volume1/docker/MusicTool/output:/app/output \
  -v /volume1/docker/MusicTool/temp:/app/temp \
  -v /volume1/docker/MusicTool/uploads:/app/uploads \
  -v /volume1/music:/app/shared_music \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  musictool:amd64
```

## 方案二：本地保存镜像文件

### 1. 保存镜像为文件

```bash
# 构建镜像
docker build -t musictool:latest .

# 保存镜像为 tar 文件
docker save -o musictool-latest.tar musictool:latest
```

### 2. 上传到绿联并加载

```bash
# 在绿联上加载 AMD64 架构镜像
docker load -i musictool-amd64.tar

# 运行容器
docker run -d \
  --name music-tool-web \
  -p 5001:5000 \
  -v /volume1/docker/MusicTool/input:/app/input \
  -v /volume1/docker/MusicTool/output:/app/output \
  -v /volume1/docker/MusicTool/temp:/app/temp \
  -v /volume1/docker/MusicTool/uploads:/app/uploads \
  -v /volume1/music:/app/shared_music \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  musictool:amd64
```

## 方案三：使用 Docker Compose（推荐）

### 1. 创建 docker-compose.yml

```yaml
services:
  music-tool:
    image: musictool:amd64  # 使用 AMD64 架构镜像
    container_name: music-tool-web
    ports:
      - "5001:5000"
    volumes:
      - /volume1/docker/MusicTool/input:/app/input
      - /volume1/docker/MusicTool/output:/app/output
      - /volume1/docker/MusicTool/temp:/app/temp
      - /volume1/docker/MusicTool/uploads:/app/uploads
      - /volume1/music:/app/shared_music
    environment:
      - TZ=Asia/Shanghai
      - PYTHONPATH=/app
      - PYTHONIOENCODING=utf-8
      - FLASK_ENV=production
    restart: unless-stopped
```

### 2. 启动服务

```bash
docker-compose up -d
```

## 访问方式

部署完成后，您可以通过以下地址访问：
- http://[绿联IP]:5001

## 目录说明

- `/volume1/docker/MusicTool/input`: 输入文件目录
- `/volume1/docker/MusicTool/output`: 输出文件目录  
- `/volume1/docker/MusicTool/temp`: 临时文件目录
- `/volume1/docker/MusicTool/uploads`: 上传文件目录
- `/volume1/music`: 绿联音乐共享目录（可选）

## 常用命令

```bash
# 查看容器状态
docker ps

# 查看容器日志
docker logs music-tool-web

# 停止容器
docker stop music-tool-web

# 重启容器
docker restart music-tool-web

# 更新镜像
docker pull makotome/musictool:latest
docker stop music-tool-web
docker rm music-tool-web
# 然后重新运行容器命令
```
