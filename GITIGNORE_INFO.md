# Git 忽略文件说明

本项目的 `.gitignore` 文件配置说明：

## 🎵 忽略的音频文件类型

- **常见音频格式**: `*.mp3`, `*.flac`, `*.wav`, `*.m4a`, `*.m4s`, `*.aac`, `*.ogg` 等
- **音频输出目录**: `mp3_output/`, `wav_output/`, `donglihuoche1/` 等
- **音频项目文件**: `*.cue`, `*.log`, `*.bin` 等

## 🗂️ 忽略的系统和临时文件

- **Python 缓存**: `__pycache__/`, `*.pyc`, `*.pyo` 等
- **系统文件**: `.DS_Store` (macOS), `Thumbs.db` (Windows)
- **IDE 文件**: `.vscode/`, `.idea/` 等
- **日志文件**: `*.log`, `m4s_conversion.log` 等
- **临时文件**: `*.tmp`, `*.bak`, `*.backup` 等

## 📦 忽略的其他文件

- **虚拟环境**: `venv/`, `.env` 等
- **构建文件**: `build/`, `dist/`, `*.egg-info/` 等
- **压缩文件**: `*.zip`, `*.rar`, `*.7z` 等

## ✅ 会被提交到 Git 的文件

- Python 源代码 (`*.py`)
- 文档文件 (`*.md`)
- 配置文件 (`requirements.txt`)
- 项目说明和示例文件

这样配置确保：
1. 📁 **仓库保持精简**: 不包含大体积的音频文件
2. 🔒 **隐私保护**: 不上传个人音乐收藏
3. ⚡ **传输高效**: 大幅减少 clone 和 pull 的时间
4. 🧹 **环境清洁**: 排除临时文件和系统特定文件
