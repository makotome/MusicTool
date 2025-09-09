# M4S to MP3 批量转换工具

## 快速开始

**最简单的使用方法：**

```bash
python convert_m4s.py
```

这个命令会自动将 `m4s` 文件夹中的所有 m4s 文件转换为 mp3 格式，并保存到 `mp3_output` 文件夹中。

## 项目文件说明

- **`convert_m4s.py`** - 🚀 **推荐使用**：一键转换脚本，最简单易用
- **`m4s_to_mp3_ffmpeg.py`** - 核心转换器（FFmpeg 版本），稳定可靠
- **`m4s_to_mp3_converter.py`** - 备用转换器（Pydub 版本）
- **`test_m4s_ffmpeg.py`** - 测试脚本，支持交互式选择
- **`M4S_TO_MP3_USAGE.md`** - 详细使用说明文档

## 转换结果

✅ **测试成功**: 已成功转换 117 个 m4s 文件为 mp3 格式
- 转换成功率: 100%
- 音质: 192kbps MP3
- 支持中文文件名
- 自动处理文件夹结构

## 系统要求

- Python 3.7+
- FFmpeg（已安装 ✅）
- macOS/Linux/Windows

## 使用示例

```bash
# 一键转换（推荐）
python convert_m4s.py

# 交互式转换（可选择是否继续）
python test_m4s_ffmpeg.py

# 手动指定目录
python m4s_to_mp3_ffmpeg.py source_folder output_folder
```

## 功能特性

- 🚀 **一键转换**: 简单命令即可批量转换
- 📁 **智能目录管理**: 自动创建输出目录
- 🎵 **高质量音频**: 192kbps MP3 输出
- 📝 **详细日志**: 完整的转换日志记录
- 🔄 **错误恢复**: 单个文件失败不影响整体转换
- 🌐 **多语言支持**: 完美支持中文等各种字符
- ⚡ **高性能**: 使用 FFmpeg 确保转换速度和质量

## 输出文件位置

转换后的 mp3 文件会保存在 `mp3_output` 文件夹中，保持原有的文件名（仅扩展名改为 .mp3）。

---

💡 **提示**: 如需详细配置说明，请查看 `M4S_TO_MP3_USAGE.md` 文件。
