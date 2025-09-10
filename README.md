# 音乐处理工具集 🎵

一个功能丰富的音乐处理工具项目，提供多种音频处理功能。本项目采用 Python 开发，支持多种音频格式，为音乐爱好者和开发者提供便捷的音频处理解决方案。

## 📋 功能列表

### 🎯 已实现功能

#### 1. 音乐分割切除工具
- **文件**: `flac_splitter.py`
- **功能**: 根据 CUE 文件自动分割音频文件
- **支持格式**: FLAC, WAV 等
- **特性**:
  - 支持中文编码检测
  - 自动创建分割后的音轨文件
  - 保留音频元数据信息
  - 支持批量处理

#### 2. M4S 转 MP3 工具
- **文件**: `m4s_to_mp3_ffmpeg.py`, `convert_m4s.py`
- **功能**: 批量转换 M4S 文件为 MP3 格式
- **特性**:
  - 一键批量转换
  - 高质量 MP3 输出 (192kbps)
  - 完美支持中文文件名
  - 详细转换日志
  - 错误恢复机制

### 🚀 计划中的功能

- 音频格式转换（MP3 ↔ FLAC ↔ WAV ↔ M4A）
- 音频元数据编辑
- 音频质量分析
- 批量重命名工具
- 音频合并工具
- 音频降噪处理
- 音频标准化/音量调节

## 🛠️ 使用方法

### 音乐分割工具

```bash
# 分割 FLAC 文件
python flac_splitter.py
```

详细说明请参考: [FLAC_USAGE.md](FLAC_USAGE.md)

### M4S 转 MP3 工具

```bash
# 一键转换（推荐）
python convert_m4s.py

# 交互式转换
python test_m4s_ffmpeg.py
```

详细说明请参考: [M4S_TO_MP3_USAGE.md](M4S_TO_MP3_USAGE.md)

## 📦 依赖安装

### 系统要求
- Python 3.7+
- FFmpeg（用于音频处理）

### Python 依赖

```bash
pip install -r requirements.txt
```

### FFmpeg 安装

```bash
# macOS (使用 Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载并安装
```

## 📁 项目结构

```
音乐处理工具集/
├── README.md                    # 项目总览（本文件）
├── requirements.txt             # Python 依赖列表
│
├── 音乐分割功能/
│   ├── flac_splitter.py        # FLAC 分割器
│   └── FLAC_USAGE.md           # 详细使用说明
│
├── M4S转MP3功能/
│   ├── convert_m4s.py          # 一键转换脚本（推荐）
│   ├── m4s_to_mp3_ffmpeg.py    # FFmpeg 版本转换器
│   ├── m4s_to_mp3_converter.py # Pydub 版本转换器
│   ├── test_m4s_ffmpeg.py      # 转换测试脚本
│   ├── test_m4s_converter.py   # 转换器测试
│   ├── M4S_TO_MP3_USAGE.md     # 详细使用说明
│   └── M4S_CONVERTER_README.md # 功能总览
│
├── 缓存文件/
│   └── __pycache__/            # Python 缓存
│
└── 示例数据/
    ├── CD2.cue                 # CUE 文件示例
    ├── CD2.wav                 # 音频文件示例
    ├── m4s/                    # M4S 文件目录
    ├── mp3_output/             # MP3 输出目录
    ├── wav_output/             # WAV 输出目录
    ├── donglihuoche1/          # 分割后的音乐文件
    └── m4s_conversion.log      # 转换日志文件
```

## ⚡ 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd 音乐处理工具集
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 选择功能
```bash
# 音乐分割
python flac_splitter.py

# M4S 转 MP3
python convert_m4s.py
```

## 🎯 使用场景

- **音乐收藏整理**: 将完整专辑分割为单独曲目
- **格式转换**: 将各种音频格式转换为常用的 MP3
- **批量处理**: 一次性处理大量音频文件
- **音质保持**: 使用高质量编码保持音频品质
- **自动化工作流**: 集成到音乐管理系统中

## � Docker 部署

本项目支持 Docker 容器化部署，一键启动即可使用！

### 快速开始

```bash
# 1. 构建并启动容器
./docker-manage.sh build
./docker-manage.sh start

# 2. 进入容器使用工具
./docker-manage.sh shell

# 3. 或直接运行工具
./docker-manage.sh flac    # FLAC 分割
./docker-manage.sh m4s     # M4S 转换
```

### Docker 优势

- ✅ **零依赖安装**: 无需手动安装 Python、FFmpeg 等依赖
- ✅ **环境隔离**: 不影响宿主机环境
- ✅ **跨平台**: 支持 Windows、macOS、Linux
- ✅ **一键部署**: 简化的部署和使用流程
- ✅ **数据持久化**: 处理结果自动保存到宿主机

详细说明请参考: [DOCKER_USAGE.md](DOCKER_USAGE.md)

## �🔧 技术特性

- **多格式支持**: FLAC, WAV, M4S, MP3 等
- **编码检测**: 自动检测和处理各种字符编码
- **错误处理**: 完善的异常处理和恢复机制
- **日志记录**: 详细的操作日志和进度跟踪
- **跨平台**: 支持 Windows, macOS, Linux
- **高性能**: 使用 FFmpeg 确保处理速度和质量
- **容器化**: Docker 支持，简化部署和使用

## 📝 开发计划

### 短期目标
- [ ] 添加音频格式转换功能
- [ ] 实现音频元数据编辑
- [ ] 创建图形用户界面 (GUI)

### 长期目标
- [ ] 音频质量分析工具
- [ ] 智能音乐标签识别
- [ ] 云端处理支持
- [ ] 插件系统架构

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- Email: [您的邮箱]

---

⭐ 如果这个项目对您有帮助，请给它一个星标！