# M4S to MP3 转换器使用说明

## 功能介绍

这个程序可以将 m4s 格式的音频文件批量转换为 mp3 格式。m4s 文件通常是从流媒体平台下载的音频片段，实际上是 mp4 音频容器的一种变体。

## 可用版本

本工具提供了两个版本：

1. **FFmpeg 版本** (`m4s_to_mp3_ffmpeg.py`) - **推荐使用**
   - 直接调用 ffmpeg 命令行工具
   - 更好的兼容性，特别是在 Python 3.13+ 环境中
   - 更稳定的转换质量
   - 支持更多音频格式

2. **Pydub 版本** (`m4s_to_mp3_converter.py`)
   - 使用 Python pydub 库
   - 可能在某些 Python 版本中存在兼容性问题

## 依赖安装

在使用转换器之前，需要安装必要的依赖：

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 ffmpeg（pydub 需要）
# macOS (使用 Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载并安装
```

## 使用方法

### 基本用法（推荐使用 FFmpeg 版本）

```bash
# 使用 FFmpeg 版本转换 m4s 文件夹中的所有文件到 mp3_output 文件夹
python m4s_to_mp3_ffmpeg.py

# 指定源目录
python m4s_to_mp3_ffmpeg.py m4s

# 指定源目录和输出目录
python m4s_to_mp3_ffmpeg.py m4s my_mp3_files
```

### 备用方法（Pydub 版本）

```bash
# 转换 m4s 文件夹中的所有文件到 mp3_output 文件夹
python m4s_to_mp3_converter.py

# 指定源目录
python m4s_to_mp3_converter.py m4s

# 指定源目录和输出目录
python m4s_to_mp3_converter.py m4s my_mp3_files
```

### 程序特性

1. **批量转换**: 自动处理整个目录中的所有 m4s 文件
2. **智能格式检测**: 自动尝试不同的音频格式解析方式
3. **详细日志**: 记录转换过程和结果到日志文件
4. **错误处理**: 继续处理其他文件，即使某些文件转换失败
5. **进度显示**: 实时显示转换进度
6. **结果统计**: 转换完成后显示详细的成功/失败统计

### 输出文件

- 转换后的 mp3 文件会保存在指定的输出目录中
- 文件名保持原有的基础名称，只改变扩展名
- mp3 文件使用 192k 比特率，平衡音质和文件大小
- 会自动添加基本的元数据标签

### 日志文件

程序会生成 `m4s_conversion.log` 日志文件，包含：
- 转换过程的详细记录
- 错误信息和失败原因
- 时间戳和进度信息

## 示例

假设您的 m4s 文件结构如下：
```
m4s/
├── 001.風の住む街 - 磯村由紀子.m4s
├── 002.城南花已开 - 三亩地.m4s
└── 003.青空 - Candy_Wind.m4s
```

运行转换器后：
```
mp3_output/
├── 001.風の住む街 - 磯村由紀子.mp3
├── 002.城南花已开 - 三亩地.mp3
└── 003.青空 - Candy_Wind.mp3
```

## 故障排除

### 常见问题

1. **"无法解析导入pydub"错误**
   - 确保已安装 pydub: `pip install pydub`
   - 确保已安装 ffmpeg

2. **"ffmpeg not found"错误**
   - 安装 ffmpeg 并确保它在系统 PATH 中
   - 重启终端/命令提示符

3. **某些文件转换失败**
   - 检查日志文件了解具体错误
   - 确认 m4s 文件没有损坏
   - 某些 DRM 保护的文件可能无法转换

4. **内存不足**
   - 对于大文件，可能需要更多内存
   - 考虑分批处理文件

### 性能优化

- 对于大量文件，建议分批处理
- 确保有足够的磁盘空间存储转换后的文件
- SSD 硬盘会显著提高转换速度

## 注意事项

1. **版权声明**: 请确保您有权转换这些音频文件，遵守相关版权法律
2. **文件备份**: 建议在转换前备份原始文件
3. **质量损失**: 转换过程可能会有轻微的音质损失
4. **文件大小**: mp3 文件通常比原始 m4s 文件略小

## 技术说明

- 使用 pydub 库进行音频处理
- 支持多种音频格式的自动检测
- 使用 pathlib 进行跨平台路径处理
- 包含完整的异常处理和日志记录
