# 音频切割工具使用说明

## 简介
这是一个用于切割音频文件的工具，支持FLAC和WAV格式，根据CUE文件信息自动切割成单独的歌曲文件。

## 功能特点
- ✅ 支持FLAC和WAV格式音频文件
- ✅ 自动解析CUE文件（支持中文编码）
- ✅ 保持原始音质（FLAC无损压缩，WAV无损PCM）
- ✅ 根据CUE信息自动命名文件
- ✅ 简单易用，无需复杂配置

## 系统要求
1. **Python 3.6+**
2. **ffmpeg** (音频处理工具)
   ```bash
   # macOS安装ffmpeg
   brew install ffmpeg
   ```
3. **Python依赖**
   ```bash
   pip install chardet
   ```

## 使用方法

### 方法1: 自动模式（推荐）
将音频文件（FLAC或WAV）和CUE文件放在同一目录下，直接运行：

```bash
python flac_splitter.py
```

工具会自动找到目录中的音频文件和CUE文件进行处理。

### 方法2: 手动指定文件
```bash
# 处理FLAC文件
python flac_splitter.py your_album.flac your_album.cue

# 处理WAV文件
python flac_splitter.py your_album.wav your_album.cue
```

### 方法3: 指定输出目录
```bash
python flac_splitter.py your_album.flac your_album.cue "我的音乐"
python flac_splitter.py your_album.wav your_album.cue "我的音乐"
```

## 文件命名规则
生成的文件名格式：`轨道号. 艺术家 - 歌曲标题.格式`

例如：
- `01. 周杰伦 - 青花瓷.flac`（FLAC输入）
- `02. 周杰伦 - 夜曲.wav`（WAV输入）

## 目录结构示例
```
你的音乐目录/
├── album.flac          # 完整专辑文件（FLAC格式）
├── album.cue           # CUE信息文件
├── CD2.wav             # 完整专辑文件（WAV格式）
├── CD2.cue             # 对应的CUE文件
├── flac_splitter.py    # 切割工具
├── 切割后的歌曲/        # FLAC输出目录
│   ├── 01. 艺术家 - 歌曲1.flac
│   └── 02. 艺术家 - 歌曲2.flac
└── wav_output/         # WAV输出目录
    ├── 01. 艺术家 - 歌曲1.wav
    └── 02. 艺术家 - 歌曲2.wav
```

## 支持的CUE文件格式
标准CUE文件，包含以下信息：
- PERFORMER（艺术家）
- TITLE（专辑/歌曲标题）
- FILE（音频文件名）
- TRACK（轨道信息）
- INDEX 01（开始时间点）

## 支持的音频格式

### 输入格式
- **FLAC**: 无损压缩音频格式
- **WAV**: 无损PCM音频格式

### 输出格式
- **FLAC输入** → **FLAC输出**: 保持无损压缩，compression_level=5
- **WAV输入** → **WAV输出**: 16位PCM编码，保持无损音质

## 注意事项
1. 确保音频文件（FLAC或WAV）和CUE文件在同一目录
2. CUE文件中的FILE字段应该指向正确的音频文件名
3. 处理大文件时需要足够的磁盘空间
4. 建议备份原始文件
5. WAV文件通常比FLAC文件大，确保有足够存储空间

## 常见问题

**Q: 提示"未找到ffmpeg命令"怎么办？**
A: 需要安装ffmpeg：`brew install ffmpeg`

**Q: CUE文件出现乱码怎么办？**
A: 工具会自动检测编码，如仍有问题，可将CUE文件转换为UTF-8编码

**Q: 可以处理其他格式吗？**
A: 目前支持FLAC和WAV格式，这两种都是无损音频格式，能保证最佳音质

## 快速测试
使用提供的示例文件测试：
```bash
python flac_splitter.py
# 会处理example_album.cue（如果有对应的FLAC文件）
```
