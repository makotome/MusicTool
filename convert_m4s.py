#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速 M4S 转换脚本
一键转换 m4s 文件夹中的所有文件为 mp3
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from m4s_to_mp3_ffmpeg import M4SToMP3ConverterFFmpeg

def main():
    """主函数 - 快速转换"""
    print("🎵 M4S to MP3 快速转换工具 🎵")
    print("="*40)
    
    # 检查源目录
    source_dir = Path("m4s")
    if not source_dir.exists():
        print("❌ 错误：找不到 'm4s' 文件夹")
        print("请确保当前目录下有 'm4s' 文件夹，并包含要转换的 .m4s 文件")
        return
    
    # 检查是否有 m4s 文件
    m4s_files = list(source_dir.glob("*.m4s"))
    if not m4s_files:
        print("❌ 错误：m4s 文件夹中没有找到 .m4s 文件")
        return
    
    print(f"✅ 找到 {len(m4s_files)} 个 m4s 文件待转换")
    print(f"📁 源目录: {source_dir.absolute()}")
    print(f"📁 输出目录: mp3_output")
    print("-"*40)
    
    # 显示前几个文件示例
    print("文件示例:")
    for i, file in enumerate(m4s_files[:3], 1):
        print(f"  {i}. {file.name}")
    if len(m4s_files) > 3:
        print(f"  ... 还有 {len(m4s_files) - 3} 个文件")
    
    print("-"*40)
    print("🚀 开始自动转换...")
    
    # 执行转换
    converter = M4SToMP3ConverterFFmpeg("m4s", "mp3_output")
    success = converter.convert_all_files()
    
    if success:
        print("\n🎉 转换完成！")
        print(f"📂 转换后的 mp3 文件保存在: {Path('mp3_output').absolute()}")
        print("\n💡 提示：")
        print("  - 转换日志保存在 m4s_conversion.log")
        print("  - 如有问题，请查看日志文件获取详细信息")
    else:
        print("\n❌ 转换过程中遇到问题")
        print("请查看 m4s_conversion.log 日志文件获取详细信息")

if __name__ == "__main__":
    main()
