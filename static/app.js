// 音乐处理工具 Web 界面 JavaScript

let currentTool = null;
let selectedFiles = [];
let currentTaskId = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function () {
    loadSystemInfo();
    loadTaskHistory();

    // 设置文件拖拽
    setupFileDrop();

    // 设置文件选择
    setupFileInput();

    // 定期更新任务状态
    setInterval(updateTaskStatus, 2000);
});

// 选择工具
function selectTool(tool) {
    currentTool = tool;
    selectedFiles = [];

    // 更新界面
    document.getElementById('tool-workspace').style.display = 'block';
    document.getElementById('progress-container').style.display = 'none';

    if (tool === 'flac') {
        document.getElementById('tool-title').textContent = '音频分割 - 选择文件';
        document.querySelector('#file-drop-zone h5').textContent = '选择音频文件和 CUE 文件';
        document.querySelector('#file-drop-zone p').textContent = '支持 FLAC、WAV 格式，需要同时提供音频文件和对应的 CUE 文件';
    } else if (tool === 'm4s') {
        document.getElementById('tool-title').textContent = 'M4S 转换 - 选择文件';
        document.querySelector('#file-drop-zone h5').textContent = '选择 M4S 文件';
        document.querySelector('#file-drop-zone p').textContent = '支持批量选择 M4S 文件进行转换';
    }

    // 刷新文件列表 - 现有文件功能已移除
    // refreshFiles();
    updateStartButton();

    // 滚动到工具区域
    document.getElementById('tool-workspace').scrollIntoView({ behavior: 'smooth' });
}

// 设置文件拖拽
function setupFileDrop() {
    const dropZone = document.getElementById('file-drop-zone');

    dropZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', function (e) {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', function (e) {
        e.preventDefault();
        dropZone.classList.remove('dragover');

        const files = Array.from(e.dataTransfer.files);
        handleFileSelection(files);
    });
}

// 设置文件输入
function setupFileInput() {
    const fileInput = document.getElementById('file-input');

    fileInput.addEventListener('change', function (e) {
        const files = Array.from(e.target.files);
        handleFileSelection(files);
    });
}

// 处理文件选择
function handleFileSelection(files) {
    if (!currentTool) {
        alert('请先选择处理工具');
        return;
    }

    // 过滤文件类型
    let validFiles = [];
    if (currentTool === 'flac') {
        // 支持的音频格式
        const supportedAudioFormats = ['.flac', '.wav'];
        const plannedFormats = ['.ape', '.mp3', '.ogg', '.m4a']; // 计划支持的格式

        validFiles = files.filter(f => {
            const fileName = f.name.toLowerCase();
            return supportedAudioFormats.some(ext => fileName.endsWith(ext)) || fileName.endsWith('.cue');
        });

        // 检查是否有不支持的格式
        const unsupportedFiles = files.filter(f => {
            const fileName = f.name.toLowerCase();
            return plannedFormats.some(ext => fileName.endsWith(ext));
        });

        if (unsupportedFiles.length > 0) {
            const unsupportedFormats = [...new Set(unsupportedFiles.map(f => {
                const ext = f.name.toLowerCase().match(/\.[^.]+$/);
                return ext ? ext[0].toUpperCase() : '';
            }))];
            alert(`检测到暂不支持的格式: ${unsupportedFormats.join(', ')}\n\n当前支持: FLAC, WAV\n计划支持: APE, MP3, OGG, M4A`);
        }
    } else if (currentTool === 'm4s') {
        validFiles = files.filter(f => f.name.toLowerCase().endsWith('.m4s'));
    }

    if (validFiles.length === 0) {
        alert('请选择正确的文件类型');
        return;
    }

    // 上传文件
    uploadFiles(validFiles);
}

// 上传文件
function uploadFiles(files) {
    const formData = new FormData();
    files.forEach(file => {
        formData.append('files', file);
    });

    // 显示上传进度容器
    const progressContainer = document.getElementById('upload-progress-container');
    const progressBar = document.getElementById('upload-progress-bar');
    const progressText = document.getElementById('upload-progress-text');

    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    progressText.textContent = '0%';

    showLoadingMessage('上传文件中...');

    // 创建XMLHttpRequest以支持进度显示
    const xhr = new XMLHttpRequest();

    // 监听上传进度
    xhr.upload.addEventListener('progress', function (e) {
        if (e.lengthComputable) {
            const percentComplete = Math.round((e.loaded / e.total) * 100);
            progressBar.style.width = percentComplete + '%';
            progressBar.setAttribute('aria-valuenow', percentComplete);
            progressText.textContent = percentComplete + '%';
        }
    });

    // 处理上传完成
    xhr.addEventListener('load', function () {
        progressContainer.style.display = 'none';

        if (xhr.status === 200) {
            try {
                const data = JSON.parse(xhr.responseText);
                if (data.error) {
                    throw new Error(data.error);
                }

                // 添加到选中文件列表
                selectedFiles = selectedFiles.concat(data.uploaded_files);
                updateSelectedFiles();
                updateStartButton();

                showSuccessMessage(`成功上传 ${data.uploaded_files.length} 个文件`);
            } catch (error) {
                showErrorMessage('文件上传失败: ' + error.message);
            }
        } else {
            showErrorMessage('上传失败，服务器响应错误');
        }
    });

    // 处理上传错误
    xhr.addEventListener('error', function () {
        progressContainer.style.display = 'none';
        showErrorMessage('文件上传失败: 网络错误');
    });

    // 发送请求
    xhr.open('POST', '/api/upload');
    xhr.send(formData);
}

// 刷新文件列表 - 功能已移除，仅保留文件上传
function refreshFiles() {
    // 现有文件功能已移除，只显示上传的文件
    console.log('现有文件功能已移除');
}

// 显示现有文件 - 功能已移除
function displayExistingFiles(files) {
    // 现有文件功能已移除
    console.log('现有文件功能已移除');
}

// 切换文件选择 - 功能已移除
function toggleFileSelection(button) {
    // 现有文件功能已移除
    console.log('现有文件功能已移除');
}

// 更新已选择文件显示
function updateSelectedFiles() {
    const container = document.getElementById('selected-files-container');
    const filesList = document.getElementById('selected-files');

    if (selectedFiles.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';

    let html = '';
    selectedFiles.forEach((file, index) => {
        const icon = getFileIcon(file.type || getFileExtension(file.name));
        const size = formatFileSize(file.size);

        html += `
            <div class="file-item">
                <div class="d-flex align-items-center">
                    <i class="${icon} me-2"></i>
                    <div>
                        <div class="fw-medium">${file.name}</div>
                        <small class="text-muted">${size}</small>
                    </div>
                </div>
                <button class="btn btn-sm btn-outline-danger" onclick="removeSelectedFile(${index})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    });

    filesList.innerHTML = html;
}

// 移除已选择文件
function removeSelectedFile(index) {
    selectedFiles.splice(index, 1);
    updateSelectedFiles();
    updateStartButton();
    // refreshFiles(); // 刷新文件列表以更新选择状态 - 现有文件功能已移除
}

// 更新开始按钮状态
function updateStartButton() {
    const button = document.getElementById('start-processing');
    const canStart = selectedFiles.length > 0 && validateFileSelection();

    button.disabled = !canStart;

    if (!canStart && selectedFiles.length > 0) {
        if (currentTool === 'flac') {
            const supportedAudioFormats = ['.flac', '.wav'];
            const hasAudio = selectedFiles.some(f => {
                const fileName = f.name.toLowerCase();
                return supportedAudioFormats.some(ext => fileName.endsWith(ext));
            });
            const hasCue = selectedFiles.some(f => f.name.toLowerCase().endsWith('.cue'));
            if (!hasAudio || !hasCue) {
                button.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>需要音频文件(FLAC/WAV)和CUE文件';
            }
        }
    } else if (canStart) {
        button.innerHTML = '<i class="fas fa-play me-2"></i>开始处理';
    }
}

// 验证文件选择
function validateFileSelection() {
    if (selectedFiles.length === 0) return false;

    if (currentTool === 'flac') {
        // 检查是否有支持的音频格式
        const supportedAudioFormats = ['.flac', '.wav'];
        const hasAudio = selectedFiles.some(f => {
            const fileName = f.name.toLowerCase();
            return supportedAudioFormats.some(ext => fileName.endsWith(ext));
        });
        const hasCue = selectedFiles.some(f => f.name.toLowerCase().endsWith('.cue'));
        return hasAudio && hasCue;
    } else if (currentTool === 'm4s') {
        return selectedFiles.some(f => f.name.toLowerCase().endsWith('.m4s'));
    }

    return false;
}

// 开始处理
function startProcessing() {
    if (!validateFileSelection()) {
        alert('请选择正确的文件');
        return;
    }

    const taskType = currentTool === 'flac' ? 'flac_split' : 'm4s_convert';
    const outputDir = document.getElementById('output-dir').value;

    const requestData = {
        type: taskType,
        input_files: selectedFiles,
        output_dir: outputDir
    };

    fetch('/api/start-task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }

            currentTaskId = data.task_id;
            document.getElementById('progress-container').style.display = 'block';
            document.getElementById('start-processing').disabled = true;

            showSuccessMessage('任务已启动');

            // 滚动到进度区域
            document.getElementById('progress-container').scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            showErrorMessage('启动任务失败: ' + error.message);
        });
}

// 更新任务状态
function updateTaskStatus() {
    if (!currentTaskId) return;

    fetch(`/api/task/${currentTaskId}`)
        .then(response => response.json())
        .then(task => {
            if (task.error) return;

            updateTaskDisplay(task);

            if (task.status === 'completed') {
                handleTaskCompleted(task);
            } else if (task.status === 'failed') {
                handleTaskFailed(task);
            }
        })
        .catch(error => {
            console.error('Failed to update task status:', error);
        });
}

// 更新任务显示
function updateTaskDisplay(task) {
    const statusElement = document.getElementById('task-status');
    const messageElement = document.getElementById('task-message');
    const progressTextElement = document.getElementById('task-progress-text');
    const progressBarElement = document.getElementById('task-progress-bar');

    // 更新状态样式
    statusElement.className = `task-status ${task.status}`;

    // 更新消息和进度
    messageElement.textContent = task.message;
    progressTextElement.textContent = `${task.progress}%`;
    progressBarElement.style.width = `${task.progress}%`;

    // 根据状态设置进度条颜色
    progressBarElement.className = 'progress-bar';
    if (task.status === 'completed') {
        progressBarElement.classList.add('bg-success');
    } else if (task.status === 'failed') {
        progressBarElement.classList.add('bg-danger');
    } else if (task.status === 'running') {
        progressBarElement.classList.add('bg-info');
    }
}

// 任务完成处理
function handleTaskCompleted(task) {
    currentTaskId = null;
    document.getElementById('start-processing').disabled = false;

    // 显示成功模态框
    document.getElementById('success-details').innerHTML = `
        <p><strong>处理时间:</strong> ${formatDuration(task.started_at, task.completed_at)}</p>
        <p><strong>处理文件数:</strong> ${selectedFiles.length}</p>
    `;

    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
    successModal.show();

    // 刷新任务历史
    loadTaskHistory();
}

// 任务失败处理
function handleTaskFailed(task) {
    currentTaskId = null;
    document.getElementById('start-processing').disabled = false;

    // 显示错误模态框
    document.getElementById('error-details').textContent = task.error || '未知错误';

    const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
    errorModal.show();

    // 刷新任务历史
    loadTaskHistory();
}

// 加载系统信息
function loadSystemInfo() {
    fetch('/api/system-info')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('system-info');
            container.innerHTML = `
            <div class="mb-2">
                <small class="text-muted">总任务数:</small>
                <span class="fw-bold">${data.stats.total_tasks}</span>
            </div>
            <div class="mb-2">
                <small class="text-muted">已完成:</small>
                <span class="text-success fw-bold">${data.stats.completed_tasks}</span>
            </div>
            <div class="mb-2">
                <small class="text-muted">处理中:</small>
                <span class="text-info fw-bold">${data.stats.running_tasks}</span>
            </div>
            <div class="mb-2">
                <small class="text-muted">失败:</small>
                <span class="text-danger fw-bold">${data.stats.failed_tasks}</span>
            </div>
        `;
        })
        .catch(error => {
            console.error('Failed to load system info:', error);
        });
}

// 加载任务历史
function loadTaskHistory() {
    fetch('/api/tasks')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('task-history');
            const tasks = data.tasks || [];

            if (tasks.length === 0) {
                container.innerHTML = '<div class="text-center text-muted">暂无任务记录</div>';
                return;
            }

            let html = '';
            tasks.slice(-5).reverse().forEach(task => { // 显示最近5个任务
                const icon = getTaskIcon(task.status);
                const time = new Date(task.created_at).toLocaleString();

                html += `
                <div class="d-flex align-items-center mb-2 p-2 border rounded">
                    <i class="${icon} me-2"></i>
                    <div class="flex-grow-1">
                        <div class="small fw-medium">${getTaskTypeName(task.type)}</div>
                        <div class="text-muted" style="font-size: 0.8rem;">${time}</div>
                    </div>
                    <span class="badge bg-${getStatusColor(task.status)}">${getStatusText(task.status)}</span>
                </div>
            `;
            });

            container.innerHTML = html;
        })
        .catch(error => {
            console.error('Failed to load task history:', error);
        });
}

// 工具函数

function getFileIcon(extension) {
    const iconMap = {
        '.flac': 'fas fa-file-audio text-primary',
        '.mp3': 'fas fa-file-audio text-success',
        '.m4s': 'fas fa-file-video text-warning',
        '.cue': 'fas fa-file-alt text-info',
        '.wav': 'fas fa-file-audio text-secondary'
    };

    return iconMap[extension] || 'fas fa-file text-muted';
}

function getFileExtension(filename) {
    return '.' + filename.split('.').pop().toLowerCase();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDuration(startTime, endTime) {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const duration = Math.round((end - start) / 1000);

    if (duration < 60) {
        return `${duration} 秒`;
    } else {
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        return `${minutes} 分 ${seconds} 秒`;
    }
}

function getTaskIcon(status) {
    const iconMap = {
        'pending': 'fas fa-clock text-warning',
        'running': 'fas fa-spinner fa-spin text-info',
        'completed': 'fas fa-check-circle text-success',
        'failed': 'fas fa-times-circle text-danger'
    };

    return iconMap[status] || 'fas fa-question-circle text-muted';
}

function getTaskTypeName(type) {
    const nameMap = {
        'flac_split': 'FLAC 分割',
        'm4s_convert': 'M4S 转换'
    };

    return nameMap[type] || type;
}

function getStatusColor(status) {
    const colorMap = {
        'pending': 'warning',
        'running': 'info',
        'completed': 'success',
        'failed': 'danger'
    };

    return colorMap[status] || 'secondary';
}

function getStatusText(status) {
    const textMap = {
        'pending': '等待中',
        'running': '处理中',
        'completed': '已完成',
        'failed': '失败'
    };

    return textMap[status] || status;
}

function showSuccessMessage(message) {
    console.log('Success:', message);
    // 可以添加toast通知
}

function showErrorMessage(message) {
    console.error('Error:', message);
    alert(message); // 简单的错误提示，可以改为更优雅的通知
}

function showLoadingMessage(message) {
    console.log('Loading:', message);
    // 可以添加loading指示器
}
