#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐处理工具 Web 界面
提供友好的网页界面来操作音乐处理工具
"""

import os
import sys
import json
import subprocess
import threading
import time
import re
import urllib.parse
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_unicode_filename(filename):
    """
    创建安全的Unicode文件名，支持中文、日文等
    替代werkzeug的secure_filename，保留Unicode字符
    """
    if not filename:
        return 'unnamed'
    
    # 移除路径分隔符和其他危险字符
    filename = re.sub(r'[/\\:*?"<>|]', '_', filename)
    
    # 移除控制字符
    filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
    
    # 移除开头和结尾的点和空格
    filename = filename.strip('. ')
    
    # 如果文件名为空或只有扩展名，添加默认前缀
    if not filename or filename.startswith('.'):
        filename = 'file_' + filename
    
    # 限制文件名长度（考虑UTF-8编码）
    if len(filename.encode('utf-8')) > 255:
        name, ext = os.path.splitext(filename)
        # 保留扩展名，截断主文件名
        max_name_length = 255 - len(ext.encode('utf-8')) - 10  # 留一些缓冲
        while len(name.encode('utf-8')) > max_name_length:
            name = name[:-1]
        filename = name + ext
    
    return filename

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'music-tool-secret-key'
app.config['JSON_AS_ASCII'] = False  # 支持中文JSON响应
app.config['UPLOAD_FOLDER'] = 'uploads'

# 配置目录
BASE_DIR = Path("/app")
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"
M4S_DIR = BASE_DIR / "m4s"
UPLOAD_DIR = BASE_DIR / "uploads"

# 确保目录存在
for directory in [INPUT_DIR, OUTPUT_DIR, TEMP_DIR, M4S_DIR, UPLOAD_DIR]:
    directory.mkdir(exist_ok=True)

# 任务状态存储
task_status = {}

class TaskManager:
    """任务管理器 - 支持持久化存储和详细日志"""
    
    def __init__(self):
        self.tasks = {}
        self.task_counter = 0
        self.task_state_file = BASE_DIR / "task_state.json"
        self.load_state()
    
    def save_state(self):
        """保存任务状态到文件"""
        try:
            state = {
                'tasks': self.tasks,
                'task_counter': self.task_counter
            }
            with open(self.task_state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            logger.info(f"任务状态已保存，当前任务数: {len(self.tasks)}")
        except Exception as e:
            logger.error(f"保存任务状态失败: {e}")
    
    def load_state(self):
        """从文件加载任务状态"""
        try:
            if self.task_state_file.exists():
                with open(self.task_state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                self.tasks = state.get('tasks', {})
                self.task_counter = state.get('task_counter', 0)
                logger.info(f"已加载任务状态，任务数: {len(self.tasks)}, 计数器: {self.task_counter}")
            else:
                logger.info("任务状态文件不存在，使用默认状态")
        except Exception as e:
            logger.error(f"加载任务状态失败: {e}")
            self.tasks = {}
            self.task_counter = 0
    
    def create_task(self, task_type, params):
        """创建新任务"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"
        
        task_info = {
            'id': task_id,
            'type': task_type,
            'params': params,
            'status': 'pending',
            'progress': 0,
            'message': '任务创建中...',
            'created_at': datetime.now().isoformat(),
            'started_at': None,
            'completed_at': None,
            'error': None,
            'result': None
        }
        
        self.tasks[task_id] = task_info
        self.save_state()
        logger.info(f"✅ 创建任务: {task_id}, 类型: {task_type}, 参数: {params}")
        return task_id
    
    def update_task(self, task_id, **kwargs):
        """更新任务状态"""
        if task_id in self.tasks:
            old_status = self.tasks[task_id].get('status', 'unknown')
            self.tasks[task_id].update(kwargs)
            self.save_state()
            new_status = kwargs.get('status', old_status)
            progress = kwargs.get('progress', self.tasks[task_id].get('progress', 0))
            message = kwargs.get('message', self.tasks[task_id].get('message', ''))
            logger.info(f"🔄 更新任务 {task_id}: {old_status} -> {new_status}, 进度: {progress}%, 消息: {message}")
        else:
            logger.warning(f"⚠️ 尝试更新不存在的任务: {task_id}")
    
    def get_task(self, task_id):
        """获取任务信息"""
        task = self.tasks.get(task_id)
        if task:
            logger.debug(f"📋 获取任务 {task_id}: 状态={task.get('status')}, 进度={task.get('progress')}%")
        else:
            logger.warning(f"⚠️ 任务不存在: {task_id}")
        return task
    
    def get_all_tasks(self):
        """获取所有任务"""
        tasks = list(self.tasks.values())
        logger.debug(f"📊 返回所有任务，总数: {len(tasks)}")
        return tasks

task_manager = TaskManager()

def run_audio_splitter(task_id, input_files, output_dir):
    """运行音频分割任务"""
    try:
        task_manager.update_task(task_id, status='running', started_at=datetime.now().isoformat(), progress=10, message='开始音频分割...')
        
        # 检查输入文件 - 支持多种音频格式
        supported_audio_extensions = ['.flac', '.wav']  # 当前支持的格式
        planned_extensions = ['.ape', '.mp3', '.ogg', '.m4a']  # 计划支持的格式
        
        audio_files = [str(f) for f in input_files if any(str(f).lower().endswith(ext) for ext in supported_audio_extensions)]
        cue_files = [str(f) for f in input_files if str(f).lower().endswith('.cue')]
        
        if not audio_files or not cue_files:
            raise ValueError("需要同时提供音频文件（FLAC/WAV）和 CUE 文件")
        
        # 统计文件类型
        format_counts = {}
        for ext in supported_audio_extensions:
            count = len([f for f in audio_files if f.lower().endswith(ext)])
            if count > 0:
                format_counts[ext.upper().replace('.', '')] = count
        
        format_summary = ', '.join([f"{count}个{fmt}" for fmt, count in format_counts.items()])
        task_manager.update_task(task_id, progress=30, message=f'找到 {format_summary} 和 {len(cue_files)} 个 CUE 文件')
        
        # 执行分割，传递音频文件、CUE文件和输出目录
        # 参数格式: audio_splitter.py <audio_file> <cue_file> <output_dir>
        # 上传的文件在uploads目录中，需要构建完整路径
        uploads_dir = BASE_DIR / "uploads"
        
        # 找到第一个音频文件和CUE文件的完整路径
        audio_file_path = str(uploads_dir / audio_files[0])
        cue_file_path = str(uploads_dir / cue_files[0])
        
        logger.info(f"📂 音频文件路径: {audio_file_path}")
        logger.info(f"📂 CUE文件路径: {cue_file_path}")
        logger.info(f"📤 输出目录: {output_dir}")
        
        cmd = [sys.executable, str(BASE_DIR / "scripts" / "audio_splitter.py"), audio_file_path, cue_file_path, output_dir]
        logger.info(f"🚀 执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, encoding='utf-8')
        
        task_manager.update_task(task_id, progress=80, message='音频分割处理中...')
        
        if result.returncode == 0:
            task_manager.update_task(
                task_id, 
                status='completed', 
                progress=100, 
                message='音频分割完成', 
                completed_at=datetime.now().isoformat(),
                result={'stdout': result.stdout, 'stderr': result.stderr}
            )
        else:
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
            
    except Exception as e:
        logger.error(f"FLAC 分割任务失败: {e}")
        task_manager.update_task(
            task_id, 
            status='failed', 
            progress=0, 
            message=f'任务失败: {str(e)}',
            completed_at=datetime.now().isoformat(),
            error=str(e)
        )

def run_m4s_converter(task_id, input_files, output_dir):
    """运行 M4S 转换任务"""
    try:
        logger.info(f"🎵 开始M4S转换任务: {task_id}")
        logger.info(f"📁 输入文件数量: {len(input_files)}")
        logger.info(f"📂 输出目录: {output_dir}")
        
        task_manager.update_task(task_id, status='running', started_at=datetime.now().isoformat(), progress=10, message='开始 M4S 转换...')
        
        # 检查输入文件
        logger.info(f"🔍 检查输入文件类型...")
        input_files_str = []
        for f in input_files:
            file_str = str(f)
            input_files_str.append(file_str)
            logger.info(f"  文件: {file_str}, 是M4S: {file_str.endswith('.m4s')}")
        
        m4s_files = [f for f in input_files_str if f.endswith('.m4s')]
        logger.info(f"✅ 找到 {len(m4s_files)} 个M4S文件: {m4s_files[:3]}{'...' if len(m4s_files) > 3 else ''}")
        
        if not m4s_files:
            raise ValueError("未找到 M4S 文件")
        
        # 对于上传的文件，它们位于uploads目录中
        uploads_dir = BASE_DIR / "uploads"
        logger.info(f"📂 上传文件目录: {uploads_dir}")
        
        # 确保所有M4S文件都存在于uploads目录中
        full_path_m4s_files = []
        for m4s_file in m4s_files:
            # 如果是相对路径，则添加uploads目录
            if not os.path.isabs(m4s_file):
                full_path = uploads_dir / m4s_file
            else:
                full_path = Path(m4s_file)
            
            if full_path.exists():
                full_path_m4s_files.append(str(full_path))
                logger.info(f"  ✅ 文件存在: {full_path}")
            else:
                logger.warning(f"  ⚠️ 文件不存在: {full_path}")
        
        if not full_path_m4s_files:
            raise ValueError("所有 M4S 文件都不存在")
        
        # 使用uploads目录作为源目录
        source_dir = str(uploads_dir)
        logger.info(f"📂 源目录: {source_dir}")
        
        task_manager.update_task(task_id, progress=30, message=f'找到 {len(m4s_files)} 个 M4S 文件')
        
        # 准备转换环境
        logger.info(f"🔧 准备执行M4S转换脚本...")
        m4s_script = BASE_DIR / "scripts" / "m4s_to_mp3_ffmpeg.py"
        logger.info(f"📜 脚本路径: {m4s_script}")
        logger.info(f"📂 脚本是否存在: {m4s_script.exists()}")
        
        if not m4s_script.exists():
            raise FileNotFoundError(f"M4S转换脚本不存在: {m4s_script}")
        
        # 设置工作目录和环境变量
        work_dir = BASE_DIR
        env = os.environ.copy()
        env['PYTHONPATH'] = str(BASE_DIR)
        
        task_manager.update_task(task_id, progress=50, message='执行转换脚本...')
        
        # 执行转换，传递源目录和输出目录参数
        cmd = [sys.executable, str(m4s_script), source_dir, output_dir]
        logger.info(f"🚀 执行命令: {' '.join(cmd)}")
        logger.info(f"📁 工作目录: {work_dir}")
        logger.info(f"📂 源目录: {source_dir}")
        logger.info(f"📤 输出目录: {output_dir}")
        
        result = subprocess.run(
            cmd, 
            cwd=work_dir,
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            env=env,
            timeout=300  # 5分钟超时
        )
        
        logger.info(f"📊 命令执行完成，返回码: {result.returncode}")
        logger.info(f"📤 标准输出: {result.stdout[:500]}{'...' if len(result.stdout) > 500 else ''}")
        if result.stderr:
            logger.warning(f"⚠️ 标准错误: {result.stderr[:500]}{'...' if len(result.stderr) > 500 else ''}")
        
        task_manager.update_task(task_id, progress=80, message='M4S 转换处理中...')
        
        if result.returncode == 0:
            logger.info(f"✅ M4S转换成功完成")
            task_manager.update_task(
                task_id, 
                status='completed', 
                progress=100, 
                message='M4S 转换完成', 
                completed_at=datetime.now().isoformat(),
                result={
                    'stdout': result.stdout, 
                    'stderr': result.stderr,
                    'processed_files': len(m4s_files),
                    'output_dir': str(output_dir)
                }
            )
        else:
            error_msg = f"转换脚本执行失败 (返回码: {result.returncode})"
            logger.error(f"❌ {error_msg}")
            logger.error(f"📤 stdout: {result.stdout}")
            logger.error(f"📤 stderr: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
            
    except subprocess.TimeoutExpired as e:
        error_msg = "M4S转换超时（超过5分钟）"
        logger.error(f"⏰ {error_msg}")
        task_manager.update_task(
            task_id, 
            status='failed', 
            progress=0, 
            message=error_msg,
            completed_at=datetime.now().isoformat(),
            error=error_msg
        )
    except Exception as e:
        error_msg = f"M4S 转换任务失败: {str(e)}"
        logger.error(f"💥 {error_msg}")
        logger.exception("详细错误信息:")
        task_manager.update_task(
            task_id, 
            status='failed', 
            progress=0, 
            message=f'任务失败: {str(e)}',
            completed_at=datetime.now().isoformat(),
            error=str(e)
        )

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/files')
def list_files():
    """列出文件"""
    directory = request.args.get('dir', 'input')
    
    if directory == 'input':
        target_dir = INPUT_DIR
    elif directory == 'm4s':
        target_dir = M4S_DIR
    elif directory == 'output':
        target_dir = OUTPUT_DIR
    else:
        target_dir = INPUT_DIR
    
    files = []
    if target_dir.exists():
        for file_path in target_dir.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(target_dir)
                files.append({
                    'name': file_path.name,
                    'path': str(rel_path),
                    'size': file_path.stat().st_size,
                    'type': file_path.suffix.lower(),
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
    
    return jsonify({'files': files, 'directory': directory})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传文件"""
    if 'files' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    files = request.files.getlist('files')
    uploaded_files = []
    
    for file in files:
        if file.filename == '':
            continue
        
        filename = safe_unicode_filename(file.filename)
        file_path = UPLOAD_DIR / filename
        file.save(str(file_path))
        
        uploaded_files.append({
            'name': filename,
            'path': str(file_path),
            'size': file_path.stat().st_size
        })
    
    return jsonify({'uploaded_files': uploaded_files})

@app.route('/api/start-task', methods=['POST'])
def start_task():
    """开始处理任务"""
    try:
        data = request.get_json()
        task_type = data.get('type')
        input_files = data.get('input_files', [])
        output_dir = data.get('output_dir', str(OUTPUT_DIR))
        
        logger.info(f"🚀 收到任务请求: 类型={task_type}, 文件数={len(input_files)}, 输出目录={output_dir}")
        
        if not task_type:
            return jsonify({'error': '未指定任务类型'}), 400
        
        if not input_files:
            return jsonify({'error': '未选择输入文件'}), 400
        
        # 记录输入文件信息
        logger.info(f"📁 输入文件列表:")
        for i, file_info in enumerate(input_files):
            logger.info(f"  [{i+1}] {file_info}")
        
        # 创建任务
        task_id = task_manager.create_task(task_type, {
            'input_files': input_files,
            'output_dir': output_dir
        })
        
        logger.info(f"✅ 任务创建成功: {task_id}")
        
        # 转换文件路径
        file_paths = []
        for file_info in input_files:
            if isinstance(file_info, str):
                file_path = Path(file_info)
                file_paths.append(file_path)
                logger.info(f"📄 文件路径(字符串): {file_path}")
            else:
                file_path = Path(file_info.get('path', file_info.get('name')))
                file_paths.append(file_path)
                logger.info(f"📄 文件路径(对象): {file_path}")
        
        logger.info(f"📋 最终文件路径列表: {[str(p) for p in file_paths]}")
        
        # 在后台执行任务
        if task_type == 'flac_split':
            logger.info(f"🎵 启动FLAC分割任务线程")
            thread = threading.Thread(target=run_audio_splitter, args=(task_id, file_paths, output_dir))
        elif task_type == 'm4s_convert':
            logger.info(f"🔄 启动M4S转换任务线程")
            thread = threading.Thread(target=run_m4s_converter, args=(task_id, file_paths, output_dir))
        else:
            logger.error(f"❌ 不支持的任务类型: {task_type}")
            return jsonify({'error': '不支持的任务类型'}), 400
        
        thread.daemon = True
        thread.start()
        logger.info(f"🧵 任务线程已启动: {task_id}")
        
        return jsonify({'task_id': task_id, 'message': '任务已启动'})
        
    except Exception as e:
        logger.error(f"💥 启动任务失败: {e}")
        logger.exception("详细错误信息:")
        return jsonify({'error': f'启动任务失败: {str(e)}'}), 500

@app.route('/api/task/<task_id>')
def get_task_status(task_id):
    """获取任务状态"""
    task = task_manager.get_task(task_id)
    if not task:
        return jsonify({'error': '任务不存在'}), 404
    
    return jsonify(task)

@app.route('/api/tasks')
def get_all_tasks():
    """获取所有任务"""
    tasks = task_manager.get_all_tasks()
    return jsonify({'tasks': tasks})

@app.route('/api/download/<path:filename>')
def download_file(filename):
    """下载文件"""
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        return jsonify({'error': '文件不存在'}), 404
    
    return send_file(str(file_path), as_attachment=True)

@app.route('/api/system-info')
def system_info():
    """获取系统信息"""
    info = {
        'directories': {
            'input': str(INPUT_DIR),
            'output': str(OUTPUT_DIR),
            'temp': str(TEMP_DIR),
            'm4s': str(M4S_DIR),
            'upload': str(UPLOAD_DIR)
        },
        'stats': {
            'total_tasks': len(task_manager.tasks),
            'pending_tasks': len([t for t in task_manager.tasks.values() if t['status'] == 'pending']),
            'running_tasks': len([t for t in task_manager.tasks.values() if t['status'] == 'running']),
            'completed_tasks': len([t for t in task_manager.tasks.values() if t['status'] == 'completed']),
            'failed_tasks': len([t for t in task_manager.tasks.values() if t['status'] == 'failed'])
        }
    }
    return jsonify(info)

if __name__ == '__main__':
    # 确保模板目录存在
    template_dir = BASE_DIR / "templates"
    template_dir.mkdir(exist_ok=True)
    
    static_dir = BASE_DIR / "static"
    static_dir.mkdir(exist_ok=True)
    
    print("🎵 音乐处理工具 Web 界面启动中...")
    print(f"📁 工作目录: {BASE_DIR}")
    print(f"🌐 访问地址: http://0.0.0.0:5000")
    print("📋 可用功能:")
    print("  - FLAC 文件分割")
    print("  - M4S 文件转 MP3")
    print("  - 文件上传和管理")
    print("  - 任务进度监控")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
