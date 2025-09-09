#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频切割工具
支持FLAC和WAV音频文件，配合CUE文件进行切割
"""

import os
import re
import sys
from pathlib import Path

def detect_encoding(file_path):
    """检测文件编码"""
    import chardet
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding'] or 'utf-8'

def parse_cue_file(cue_file_path):
    """解析CUE文件，提取歌曲信息"""
    print(f"正在解析CUE文件: {cue_file_path}")
    
    # 检测编码
    encoding = detect_encoding(cue_file_path)
    print(f"检测到编码: {encoding}")
    
    with open(cue_file_path, 'r', encoding=encoding) as f:
        content = f.read()
    
    # 提取专辑信息
    album_title = ""
    album_performer = ""
    audio_file = ""
    
    title_match = re.search(r'TITLE\s+"([^"]+)"', content)
    if title_match:
        album_title = title_match.group(1)
    
    performer_match = re.search(r'PERFORMER\s+"([^"]+)"', content)
    if performer_match:
        album_performer = performer_match.group(1)
    
    file_match = re.search(r'FILE\s+"([^"]+)"', content)
    if file_match:
        audio_file = file_match.group(1)
    
    print(f"专辑: {album_title}")
    print(f"艺术家: {album_performer}")
    print(f"音频文件: {audio_file}")
    
    # 提取轨道信息
    tracks = []
    track_blocks = re.findall(r'TRACK\s+(\d+)\s+AUDIO(.*?)(?=TRACK\s+\d+\s+AUDIO|$)', content, re.DOTALL)
    
    for track_num, track_content in track_blocks:
        track_num_int = int(track_num)
        track_info = {
            'number': track_num_int,
            'title': f'Track_{track_num_int:02d}',
            'performer': album_performer
        }
        
        # 提取歌曲标题
        title_match = re.search(r'TITLE\s+"([^"]+)"', track_content)
        if title_match:
            track_info['title'] = title_match.group(1)
        
        # 提取演唱者
        performer_match = re.search(r'PERFORMER\s+"([^"]+)"', track_content)
        if performer_match:
            track_info['performer'] = performer_match.group(1)
        
        # 提取开始时间
        index_match = re.search(r'INDEX\s+01\s+(\d+):(\d+):(\d+)', track_content)
        if index_match:
            minutes, seconds, frames = map(int, index_match.groups())
            # 75帧 = 1秒
            total_seconds = minutes * 60 + seconds + frames / 75
            track_info['start_time'] = total_seconds
        else:
            track_info['start_time'] = 0
        
        tracks.append(track_info)
    
    # 计算每首歌的结束时间
    for i in range(len(tracks)):
        if i < len(tracks) - 1:
            tracks[i]['duration'] = tracks[i + 1]['start_time'] - tracks[i]['start_time']
        else:
            tracks[i]['duration'] = None  # 最后一首歌到文件结束
    
    print(f"找到 {len(tracks)} 首歌曲")
    return tracks, album_title, album_performer, audio_file

def clean_filename(name):
    """清理文件名中的非法字符"""
    illegal_chars = r'[<>:"/\\|?*]'
    return re.sub(illegal_chars, '_', name).strip()

def split_audio_with_ffmpeg(audio_file, tracks, output_dir="output"):
    """使用ffmpeg切割音频文件（支持FLAC和WAV）"""
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 检测输入文件格式
    input_ext = Path(audio_file).suffix.lower()
    if input_ext == '.flac':
        output_ext = '.flac'
        codec = 'flac'
        codec_params = ['-compression_level', '5']
    elif input_ext == '.wav':
        output_ext = '.wav'
        codec = 'pcm_s16le'  # 16位PCM编码
        codec_params = []
    else:
        print(f"❌ 不支持的音频格式: {input_ext}")
        return False
    
    print(f"\n开始切割音乐...")
    print(f"输入格式: {input_ext.upper()}")
    print(f"输出格式: {output_ext.upper()}")
    print(f"输出目录: {output_dir}")
    
    for track in tracks:
        # 生成输出文件名
        track_num = track['number']
        title = clean_filename(track['title'])
        performer = clean_filename(track['performer'])
        
        if performer:
            output_filename = f"{track_num:02d}. {performer} - {title}{output_ext}"
        else:
            output_filename = f"{track_num:02d}. {title}{output_ext}"
        
        output_path = os.path.join(output_dir, output_filename)
        
        # 构建ffmpeg命令
        start_time = track['start_time']
        
        # 基础命令
        cmd = [
            'ffmpeg', '-y',  # 覆盖已存在的文件
            '-i', audio_file,
            '-ss', str(start_time)
        ]
        
        # 添加时长参数（如果有明确的结束时间）
        if track['duration']:
            cmd.extend(['-t', str(track['duration'])])
        
        # 添加编码参数
        cmd.extend(['-c:a', codec])
        cmd.extend(codec_params)
        
        # 添加输出文件
        cmd.append(output_path)
        
        print(f"正在处理: {output_filename}")
        print(f"开始时间: {start_time:.2f}秒")
        
        # 执行ffmpeg命令
        import subprocess
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ 完成: {output_filename}")
            else:
                print(f"❌ 失败: {output_filename}")
                print(f"错误信息: {result.stderr}")
        except FileNotFoundError:
            print("❌ 错误: 未找到ffmpeg命令")
            print("请确保已安装ffmpeg: brew install ffmpeg")
            return False
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            return False
    
    return True

def find_files_in_directory(directory="."):
    """在目录中查找FLAC/WAV和CUE文件"""
    flac_files = list(Path(directory).glob("*.flac"))
    wav_files = list(Path(directory).glob("*.wav"))
    audio_files = flac_files + wav_files
    cue_files = list(Path(directory).glob("*.cue"))
    
    print(f"在目录 {directory} 中找到:")
    print(f"  FLAC文件: {len(flac_files)} 个")
    for f in flac_files:
        print(f"    {f.name}")
    
    print(f"  WAV文件: {len(wav_files)} 个")
    for f in wav_files:
        print(f"    {f.name}")
    
    print(f"  CUE文件: {len(cue_files)} 个")
    for f in cue_files:
        print(f"    {f.name}")
    
    return audio_files, cue_files

def main():
    """主函数"""
    print("音频切割工具 (支持FLAC/WAV)")
    print("=" * 40)
    
    # 如果提供了命令行参数
    if len(sys.argv) >= 3:
        audio_file = sys.argv[1]
        cue_file = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "切割后的歌曲"
    else:
        # 自动查找文件
        print("正在当前目录查找文件...")
        audio_files, cue_files = find_files_in_directory()
        
        if not audio_files:
            print("❌ 未找到音频文件（FLAC或WAV）")
            return
        
        if not cue_files:
            print("❌ 未找到CUE文件")
            return
        
        # 选择第一个找到的文件
        audio_file = str(audio_files[0])
        cue_file = str(cue_files[0])
        output_dir = "切割后的歌曲"
        
        print(f"\n使用文件:")
        print(f"  音频文件: {audio_file}")
        print(f"  CUE文件: {cue_file}")
    
    # 检查文件是否存在
    if not os.path.exists(audio_file):
        print(f"❌ 音频文件不存在: {audio_file}")
        return
    
    if not os.path.exists(cue_file):
        print(f"❌ CUE文件不存在: {cue_file}")
        return
    
    try:
        # 解析CUE文件
        tracks, album_title, album_performer, cue_audio_file = parse_cue_file(cue_file)
        
        if not tracks:
            print("❌ CUE文件中未找到有效的轨道信息")
            return
        
        print(f"\n轨道列表:")
        for track in tracks:
            duration_str = f"{track['duration']:.1f}秒" if track['duration'] else "到结束"
            print(f"  {track['number']:02d}. {track['title']} ({duration_str})")
        
        # 切割音乐
        success = split_audio_with_ffmpeg(audio_file, tracks, output_dir)
        
        if success:
            print(f"\n🎉 切割完成! 文件保存在: {output_dir}")
        else:
            print(f"\n❌ 切割过程中出现错误")
    
    except Exception as e:
        print(f"❌ 处理过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
