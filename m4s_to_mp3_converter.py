#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M4S to MP3 Converter
将 m4s 格式的音频文件批量转换为 mp3 格式

作者: GitHub Copilot
日期: 2025年9月9日
"""

import os
import sys
from pathlib import Path
from pydub import AudioSegment
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('m4s_conversion.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class M4SToMP3Converter:
    """M4S 到 MP3 转换器"""
    
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
            
            # 由于 m4s 文件实际上是 mp4 音频片段，我们尝试以 mp4 格式读取
            try:
                # 首先尝试作为 mp4 读取
                audio = AudioSegment.from_file(str(m4s_file), format="mp4")
            except Exception:
                try:
                    # 如果失败，尝试作为 m4a 读取
                    audio = AudioSegment.from_file(str(m4s_file), format="m4a")
                except Exception:
                    # 最后尝试自动检测格式
                    audio = AudioSegment.from_file(str(m4s_file))
            
            # 导出为 mp3 格式
            audio.export(
                str(output_path),
                format="mp3",
                bitrate="192k",  # 设置比特率
                tags={
                    'title': m4s_file.stem,
                    'album': 'Converted from M4S'
                }
            )
            
            logging.info(f"转换完成: {mp3_filename}")
            self.converted_count += 1
            return True
            
        except Exception as e:
            logging.error(f"转换失败 {m4s_file.name}: {str(e)}")
            self.failed_count += 1
            self.failed_files.append(str(m4s_file.name))
            return False
    
    def convert_all_files(self):
        """批量转换所有 m4s 文件"""
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
    print("M4S to MP3 Converter")
    print("="*30)
    
    # 检查命令行参数
    source_dir = "m4s"
    output_dir = "mp3_output"
    
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    print(f"源目录: {source_dir}")
    print(f"输出目录: {output_dir}")
    print("-"*30)
    
    # 创建转换器并执行转换
    converter = M4SToMP3Converter(source_dir, output_dir)
    
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
