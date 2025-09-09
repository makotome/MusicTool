#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 M4S to MP3 转换器 (FFmpeg 版本)
"""

import os
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from m4s_to_mp3_ffmpeg import M4SToMP3ConverterFFmpeg

def test_converter():
    """测试转换器功能"""
    print("=== M4S to MP3 转换器测试 (FFmpeg 版本) ===")
    
    # 检查源目录
    source_dir = Path("m4s")
    if not source_dir.exists():
        print(f"❌ 源目录不存在: {source_dir}")
        return False
    
    # 检查是否有 m4s 文件
    m4s_files = list(source_dir.glob("*.m4s"))
    if not m4s_files:
        print(f"❌ 在 {source_dir} 中没有找到 m4s 文件")
        return False
    
    print(f"✅ 找到 {len(m4s_files)} 个 m4s 文件")
    
    # 显示前5个文件作为示例
    print("\n前5个文件示例:")
    for i, file in enumerate(m4s_files[:5], 1):
        print(f"  {i}. {file.name}")
    
    if len(m4s_files) > 5:
        print(f"  ... 还有 {len(m4s_files) - 5} 个文件")
    
    # 询问用户是否继续
    print(f"\n是否要转换所有 {len(m4s_files)} 个文件到 mp3 格式?")
    response = input("输入 'y' 或 'yes' 继续: ").lower().strip()
    
    if response not in ['y', 'yes']:
        print("❌ 用户取消了转换")
        return False
    
    # 执行转换
    print("\n🚀 开始转换...")
    converter = M4SToMP3ConverterFFmpeg("m4s", "mp3_output")
    success = converter.convert_all_files()
    
    if success:
        print("✅ 转换测试完成!")
        return True
    else:
        print("❌ 转换过程中遇到问题")
        return False

if __name__ == "__main__":
    test_converter()
