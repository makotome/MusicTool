#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐处理工具主入口
提供命令行接口来运行各种音乐处理功能
"""

import sys
import os
import argparse
from pathlib import Path

# 添加scripts目录到Python路径
SCRIPT_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='音乐处理工具集 - 命令行接口',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 启动Web界面
  python main.py web
  
  # 音频分割
  python main.py split audio.flac audio.cue [输出目录]
  
  # M4S转换
  python main.py m4s 输入目录 输出目录
  
  # 显示帮助
  python main.py --help
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # Web界面命令
    web_parser = subparsers.add_parser('web', help='启动Web界面')
    web_parser.add_argument('--port', '-p', type=int, default=5000, help='Web服务端口 (默认: 5000)')
    web_parser.add_argument('--host', type=str, default='127.0.0.1', help='Web服务主机 (默认: 127.0.0.1)')
    
    # 音频分割命令
    split_parser = subparsers.add_parser('split', help='音频分割功能')
    split_parser.add_argument('audio_file', help='音频文件路径 (FLAC/WAV)')
    split_parser.add_argument('cue_file', help='CUE文件路径')
    split_parser.add_argument('output_dir', nargs='?', default='切割后的歌曲', help='输出目录 (默认: 切割后的歌曲)')
    
    # M4S转换命令
    m4s_parser = subparsers.add_parser('m4s', help='M4S转MP3功能')
    m4s_parser.add_argument('input_dir', help='M4S文件输入目录')
    m4s_parser.add_argument('output_dir', help='MP3文件输出目录')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'web':
            # 启动Web界面
            print(f"🌐 启动Web界面...")
            print(f"   地址: http://{args.host}:{args.port}")
            print(f"   按 Ctrl+C 停止服务")
            
            # 导入并启动Flask应用
            from web_app import app
            app.run(host=args.host, port=args.port, debug=False)
            
        elif args.command == 'split':
            # 音频分割
            print(f"🎵 开始音频分割...")
            print(f"   音频文件: {args.audio_file}")
            print(f"   CUE文件: {args.cue_file}")
            print(f"   输出目录: {args.output_dir}")
            
            # 导入并运行分割脚本
            import audio_splitter
            sys.argv = ['audio_splitter.py', args.audio_file, args.cue_file, args.output_dir]
            audio_splitter.main()
            
        elif args.command == 'm4s':
            # M4S转换
            print(f"🔄 开始M4S转换...")
            print(f"   输入目录: {args.input_dir}")
            print(f"   输出目录: {args.output_dir}")
            
            # 导入并运行M4S转换脚本
            import m4s_to_mp3_ffmpeg
            converter = m4s_to_mp3_ffmpeg.M4SToMP3Converter(args.input_dir, args.output_dir)
            converter.convert_all_files()
            
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保所有依赖已正确安装")
    except Exception as e:
        print(f"❌ 执行出错: {e}")

if __name__ == '__main__':
    main()
