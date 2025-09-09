#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M4S to MP3 Converter (使用 FFmpeg)
将 m4s 格式的音频文件批量转换为 mp3 格式
使用 ffmpeg 命令行工具进行转换，避免 Python 3.13 兼容性问题

作者: GitHub Copilot
日期: 2025年9月9日
"""

import os
import sys
import subprocess
from pathlib import Path
import logging
import shutil

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('m4s_conversion.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class M4SToMP3ConverterFFmpeg:
    """使用 FFmpeg 的 M4S 到 MP3 转换器"""
    
    def __init__(self, source_dir="m4s", output_dir="mp3_output"):
        """
        初始化转换器
        
        Args:
            source_dir (str): 源文件目录（包含m4s文件）
            output_dir (str): 输出目录（保存mp3文件）
        """
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.converted_count = 0
        self.failed_count = 0
        self.failed_files = []
        self.ffmpeg_path = None
        
    def check_ffmpeg(self):
        """检查 ffmpeg 是否可用"""
        try:
            # 检查 ffmpeg 是否在 PATH 中
            self.ffmpeg_path = shutil.which('ffmpeg')
            if not self.ffmpeg_path:
                logging.error("未找到 ffmpeg，请确保已安装 ffmpeg 并添加到 PATH")
                return False
            
            # 测试 ffmpeg 版本
            result = subprocess.run(
                [self.ffmpeg_path, '-version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                logging.info(f"找到 FFmpeg: {version_line}")
                return True
            else:
                logging.error("ffmpeg 执行失败")
                return False
                
        except Exception as e:
            logging.error(f"检查 ffmpeg 时出错: {e}")
            return False
    
    def setup_output_directory(self):
        """创建输出目录"""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logging.info(f"输出目录已创建: {self.output_dir}")
        except Exception as e:
            logging.error(f"创建输出目录失败: {e}")
            return False
        return True
    
    def get_m4s_files(self):
        """获取所有 m4s 文件"""
        if not self.source_dir.exists():
            logging.error(f"源目录不存在: {self.source_dir}")
            return []
        
        m4s_files = list(self.source_dir.glob("*.m4s"))
        logging.info(f"找到 {len(m4s_files)} 个 m4s 文件")
        return m4s_files
    
    def convert_single_file(self, m4s_file):
        """
        转换单个 m4s 文件为 mp3
        
        Args:
            m4s_file (Path): m4s 文件路径
            
        Returns:
            bool: 转换是否成功
        """
        try:
            # 生成输出文件名
            mp3_filename = m4s_file.stem + ".mp3"
            output_path = self.output_dir / mp3_filename
            
            logging.info(f"开始转换: {m4s_file.name}")
            
            # 构建 ffmpeg 命令
            # -i: 输入文件
            # -codec:a libmp3lame: 使用 MP3 编码器
            # -b:a 192k: 设置音频比特率为 192kbps
            # -y: 覆盖输出文件（如果存在）
            cmd = [
                self.ffmpeg_path,
                '-i', str(m4s_file),
                '-codec:a', 'libmp3lame',
                '-b:a', '192k',
                '-y',  # 覆盖输出文件
                str(output_path)
            ]
            
            # 执行转换
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                logging.info(f"转换完成: {mp3_filename}")
                self.converted_count += 1
                
                # 检查输出文件是否存在且有内容
                if output_path.exists() and output_path.stat().st_size > 0:
                    return True
                else:
                    logging.error(f"输出文件为空或不存在: {mp3_filename}")
                    self.failed_count += 1
                    self.failed_files.append(str(m4s_file.name))
                    return False
            else:
                logging.error(f"转换失败 {m4s_file.name}: {result.stderr}")
                self.failed_count += 1
                self.failed_files.append(str(m4s_file.name))
                return False
                
        except subprocess.TimeoutExpired:
            logging.error(f"转换超时 {m4s_file.name}")
            self.failed_count += 1
            self.failed_files.append(str(m4s_file.name))
            return False
        except Exception as e:
            logging.error(f"转换失败 {m4s_file.name}: {str(e)}")
            self.failed_count += 1
            self.failed_files.append(str(m4s_file.name))
            return False
    
    def convert_all_files(self):
        """批量转换所有 m4s 文件"""
        # 检查 ffmpeg
        if not self.check_ffmpeg():
            return False
        
        # 设置输出目录
        if not self.setup_output_directory():
            return False
        
        # 获取所有 m4s 文件
        m4s_files = self.get_m4s_files()
        if not m4s_files:
            logging.warning("没有找到 m4s 文件")
            return False
        
        logging.info(f"开始批量转换 {len(m4s_files)} 个文件...")
        
        # 逐个转换文件
        for i, m4s_file in enumerate(m4s_files, 1):
            logging.info(f"进度: {i}/{len(m4s_files)}")
            self.convert_single_file(m4s_file)
        
        # 输出转换结果统计
        self.print_conversion_summary()
        return True
    
    def print_conversion_summary(self):
        """打印转换结果摘要"""
        total_files = self.converted_count + self.failed_count
        
        print("\n" + "="*50)
        print("转换完成摘要")
        print("="*50)
        print(f"总文件数: {total_files}")
        print(f"成功转换: {self.converted_count}")
        print(f"转换失败: {self.failed_count}")
        
        if self.failed_files:
            print("\n失败的文件:")
            for file in self.failed_files:
                print(f"  - {file}")
        
        print(f"\n输出目录: {self.output_dir.absolute()}")
        print("="*50)
        
        # 记录到日志
        logging.info(f"转换完成 - 成功: {self.converted_count}, 失败: {self.failed_count}")

def main():
    """主函数"""
    print("M4S to MP3 Converter (FFmpeg 版本)")
    print("="*40)
    
    # 检查命令行参数
    source_dir = "m4s"
    output_dir = "mp3_output"
    
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    print(f"源目录: {source_dir}")
    print(f"输出目录: {output_dir}")
    print("-"*40)
    
    # 创建转换器并执行转换
    converter = M4SToMP3ConverterFFmpeg(source_dir, output_dir)
    
    try:
        success = converter.convert_all_files()
        if success:
            print("\n✅ 批量转换任务完成!")
        else:
            print("\n❌ 转换过程中遇到问题，请查看日志文件。")
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了转换过程")
        logging.info("用户中断转换")
    except Exception as e:
        print(f"\n❌ 发生意外错误: {e}")
        logging.error(f"意外错误: {e}")

if __name__ == "__main__":
    main()
