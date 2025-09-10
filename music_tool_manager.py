#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker 环境下的音乐工具统一入口
提供简化的命令行界面，方便在容器中使用各种音乐处理工具
"""

import os
import sys
import subprocess
from pathlib import Path
import argparse

class MusicToolManager:
    """音乐工具管理器"""
    
    def __init__(self):
        self.base_dir = Path("/app")
        self.input_dir = self.base_dir / "input"
        self.output_dir = self.base_dir / "output"
        self.temp_dir = self.base_dir / "temp"
        
        # 确保目录存在
        for dir_path in [self.input_dir, self.output_dir, self.temp_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def list_input_files(self, extension=None):
        """列出输入目录中的文件"""
        if not self.input_dir.exists():
            print(f"输入目录不存在: {self.input_dir}")
            return []
        
        files = []
        for file_path in self.input_dir.rglob("*"):
            if file_path.is_file():
                if extension is None or file_path.suffix.lower() == extension.lower():
                    files.append(file_path)
        
        return files
    
    def run_flac_splitter(self, target_dir=None):
        """运行 FLAC 分割工具"""
        print("=== FLAC 分割工具 ===")
        
        if target_dir is None:
            target_dir = self.input_dir
        
        # 检查是否有 FLAC 和 CUE 文件
        flac_files = list(Path(target_dir).glob("*.flac"))
        cue_files = list(Path(target_dir).glob("*.cue"))
        
        if not flac_files:
            print(f"在 {target_dir} 中未找到 FLAC 文件")
            return False
        
        if not cue_files:
            print(f"在 {target_dir} 中未找到 CUE 文件")
            return False
        
        print(f"找到 {len(flac_files)} 个 FLAC 文件和 {len(cue_files)} 个 CUE 文件")
        
        # 切换到目标目录执行
        original_dir = os.getcwd()
        try:
            os.chdir(target_dir)
            result = subprocess.run([sys.executable, str(self.base_dir / "flac_splitter.py")], 
                                  capture_output=False)
            return result.returncode == 0
        finally:
            os.chdir(original_dir)
    
    def run_m4s_converter(self, method="ffmpeg"):
        """运行 M4S 转换工具"""
        print("=== M4S 转 MP3 工具 ===")
        
        # 检查 m4s 目录
        m4s_dir = self.base_dir / "m4s"
        if not m4s_dir.exists():
            print(f"M4S 目录不存在: {m4s_dir}")
            return False
        
        m4s_files = list(m4s_dir.glob("*.m4s"))
        if not m4s_files:
            print(f"在 {m4s_dir} 中未找到 M4S 文件")
            return False
        
        print(f"找到 {len(m4s_files)} 个 M4S 文件")
        
        # 选择转换方法
        if method == "ffmpeg":
            script_name = "m4s_to_mp3_ffmpeg.py"
        else:
            script_name = "convert_m4s.py"
        
        # 执行转换
        result = subprocess.run([sys.executable, str(self.base_dir / script_name)], 
                              capture_output=False)
        return result.returncode == 0
    
    def show_status(self):
        """显示当前状态"""
        print("=== 音乐工具容器状态 ===")
        print(f"工作目录: {self.base_dir}")
        print(f"输入目录: {self.input_dir}")
        print(f"输出目录: {self.output_dir}")
        print(f"临时目录: {self.temp_dir}")
        print()
        
        # 检查各目录的文件
        print("文件统计:")
        
        # 输入目录
        input_files = self.list_input_files()
        print(f"  输入目录: {len(input_files)} 个文件")
        
        # M4S 目录
        m4s_dir = self.base_dir / "m4s"
        if m4s_dir.exists():
            m4s_files = list(m4s_dir.glob("*.m4s"))
            print(f"  M4S 目录: {len(m4s_files)} 个文件")
        
        # 输出目录
        if self.output_dir.exists():
            output_files = list(self.output_dir.rglob("*"))
            output_files = [f for f in output_files if f.is_file()]
            print(f"  输出目录: {len(output_files)} 个文件")
        
        print()
        
        # 显示可用工具
        print("可用工具:")
        print("  1. FLAC 分割: music-tool flac")
        print("  2. M4S 转换: music-tool m4s")
        print("  3. 查看状态: music-tool status")

def main():
    parser = argparse.ArgumentParser(description="音乐处理工具容器管理器")
    parser.add_argument("command", choices=["flac", "m4s", "status", "list"], 
                       help="要执行的命令")
    parser.add_argument("--method", choices=["ffmpeg", "pydub"], default="ffmpeg",
                       help="M4S 转换方法 (默认: ffmpeg)")
    parser.add_argument("--dir", type=str, 
                       help="指定处理目录 (对 FLAC 分割有效)")
    
    args = parser.parse_args()
    
    manager = MusicToolManager()
    
    if args.command == "status":
        manager.show_status()
    
    elif args.command == "list":
        print("=== 输入文件列表 ===")
        files = manager.list_input_files()
        for file_path in files:
            print(f"  {file_path.relative_to(manager.base_dir)}")
    
    elif args.command == "flac":
        target_dir = args.dir if args.dir else None
        success = manager.run_flac_splitter(target_dir)
        if success:
            print("✅ FLAC 分割完成")
        else:
            print("❌ FLAC 分割失败")
            sys.exit(1)
    
    elif args.command == "m4s":
        success = manager.run_m4s_converter(args.method)
        if success:
            print("✅ M4S 转换完成")
        else:
            print("❌ M4S 转换失败")
            sys.exit(1)

if __name__ == "__main__":
    main()
