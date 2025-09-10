# 🎵 音乐处理工具集

一个功能完整的音乐处理工具项目，提供Web界面和命令行两种使用方式。支持音频分割、格式转换等多种功能，为音乐爱好者和开发者提供便捷的音频处理解决方案。

![Python](https://img.shields.io/badge/Python-3.6+-blue)
![Docker](https://img.shields.io/badge/Docker-supported-brightgreen)
![Web](https://img.shields.io/badge/Web-Interface-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ 功能特性

### 🎯 音频分割工具
- **支持格式**: FLAC、WAV（计划支持：APE、MP3、OGG、M4A）
- **智能解析**: 自动解析CUE文件，支持中文、日文等编码
- **保持音质**: 无损格式保持原始音质
- **自动命名**: 根据CUE信息自动命名输出文件
- **批量处理**: Web界面支持批量上传和处理

### 🔄 M4S转MP3工具
- **批量转换**: 一键转换整个目录的M4S文件
- **高质量输出**: 192kbps高质量MP3输出
- **中文支持**: 完美支持中文文件名和路径
- **错误恢复**: 智能跳过损坏文件，继续处理
- **详细日志**: 提供详细的转换进度和错误信息

### 🌐 Web界面
- **直观操作**: 点击式工具选择，拖拽文件上传
- **实时进度**: 可视化任务进度和状态监控
- **文件管理**: 智能文件类型过滤和批量选择
- **后台处理**: 任务在后台运行，不阻塞界面
- **任务历史**: 查看历史处理记录和结果

## 🚀 快速开始

### 方法1: Web界面（推荐新手）

使用Docker快速启动：

```bash
# 1. 启动Web界面
./docker-manage.sh start

# 2. 打开浏览器访问
# http://localhost:5001

# 或者直接打开浏览器
./docker-manage.sh web
```

本地运行：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动Web界面
python main.py web

# 3. 浏览器访问 http://localhost:5000
```

### 方法2: 命令行（推荐进阶用户）

```bash
# 音频分割（支持FLAC/WAV + CUE）
python main.py split album.flac album.cue 输出目录

# M4S转MP3
python main.py m4s m4s文件目录 mp3输出目录

# 查看所有命令和帮助
python main.py --help
```

### 方法3: 直接调用脚本

```bash
# 音频分割
python scripts/audio_splitter.py album.flac album.cue 输出目录

# M4S转换
python scripts/m4s_to_mp3_ffmpeg.py 输入目录 输出目录
```

## 📋 系统要求

### 基础环境
- **Python 3.6+**
- **FFmpeg** (音频处理核心)

### FFmpeg安装
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载并添加到PATH
```

### Python依赖
```bash
pip install -r requirements.txt
```

### Docker环境（可选）
- **Docker** + **Docker Compose**
- 用于Web界面容器化部署

## 🎯 详细使用指南

### 音频分割功能

#### Web界面操作
1. 点击"音频分割"工具卡片
2. 上传音频文件（FLAC/WAV）和对应的CUE文件
3. 选择输出目录
4. 点击"开始处理"
5. 等待完成，下载结果

#### 命令行操作
```bash
# 自动模式（在包含音频和CUE文件的目录中运行）
python scripts/audio_splitter.py

# 手动指定文件
python scripts/audio_splitter.py album.flac album.cue

# 指定输出目录
python scripts/audio_splitter.py album.flac album.cue "分割后的歌曲"
```

#### 支持格式
- ✅ **FLAC** - 无损音频格式，高音质
- ✅ **WAV** - 无损PCM格式，完美音质
- 🔄 **APE** - Monkey's Audio无损格式（计划支持）
- 🔄 **MP3/OGG/M4A** - 有损音频格式（计划支持）

### M4S转MP3功能

#### Web界面操作
1. 点击"M4S转换"工具卡片
2. 批量上传M4S文件
3. 选择输出目录
4. 点击"开始处理"
5. 等待完成，下载转换后的MP3文件

#### 命令行操作
```bash
# 转换指定目录中的所有M4S文件
python scripts/m4s_to_mp3_ffmpeg.py 输入目录 输出目录

# 使用默认目录（m4s -> mp3_output）
python scripts/m4s_to_mp3_ffmpeg.py
```

#### 特性说明
- **输出质量**: 192kbps AAC编码MP3
- **文件命名**: 保持原始文件名，仅更改扩展名
- **错误处理**: 自动跳过损坏或无效文件
- **进度显示**: 实时显示转换进度和统计信息

## 🐳 Docker部署

### 快速部署
```bash
# 构建镜像
./docker-manage.sh build

# 启动服务
./docker-manage.sh start

# 查看状态
./docker-manage.sh status

# 停止服务
./docker-manage.sh stop

# 重启服务
./docker-manage.sh restart
```

### 访问方式
- **Web界面**: http://localhost:5001
- **文件管理**: 容器自动挂载本地目录
  - `./input` → `/app/input` (输入文件)
  - `./output` → `/app/output` (输出文件)
  - `./uploads` → `/app/uploads` (上传文件)

### 管理命令
```bash
# 查看容器日志
./docker-manage.sh logs

# 进入容器shell
./docker-manage.sh shell

# 清理容器和镜像
./docker-manage.sh clean
```

## 📁 项目结构

```
MusicTool/
├── main.py                 # 主入口文件
├── web_app.py             # Web界面应用
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker构建文件
├── docker-compose.yml    # Docker编排文件
├── docker-manage.sh      # Docker管理脚本
├── scripts/              # 核心功能脚本
│   ├── audio_splitter.py     # 音频分割工具
│   └── m4s_to_mp3_ffmpeg.py # M4S转换工具
├── static/               # Web静态资源
├── templates/            # Web模板文件
├── docs/                 # 详细文档
├── samples/              # 示例文件
└── input/output/uploads/ # 工作目录
```

## 🛠️ 开发说明

### 本地开发
```bash
# 克隆项目
git clone https://github.com/makotome/MusicTool.git
cd MusicTool

# 安装依赖
pip install -r requirements.txt

# 安装FFmpeg
brew install ffmpeg  # macOS

# 启动开发服务器
python main.py web --host 0.0.0.0 --port 5000
```

### 添加新功能
1. 在`scripts/`目录添加功能脚本
2. 在`main.py`中添加命令行接口
3. 在`web_app.py`中添加Web API接口
4. 在前端添加对应的UI界面

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 提交Issue
- 详细描述问题现象
- 提供错误日志和环境信息
- 如果可能，提供复现步骤

### 提交代码
1. Fork项目
2. 创建特性分支
3. 提交更改
4. 创建Pull Request

## 📄 许可证

本项目基于MIT许可证开源，详见[LICENSE](LICENSE)文件。

## 🙏 致谢

- [FFmpeg](https://ffmpeg.org/) - 强大的音频处理工具
- [Flask](https://flask.palletsprojects.com/) - Web框架
- [Bootstrap](https://getbootstrap.com/) - UI组件库
