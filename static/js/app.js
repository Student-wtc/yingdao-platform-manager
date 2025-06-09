// 全局变量
let currentJobUuid = null;
let currentTaskUuid = null;
let jobStatusInterval = null;
let taskStatusInterval = null;
let applicationData = [];

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 绑定参数复选框事件
    document.getElementById('useParams').addEventListener('change', function() {
        const paramsContainer = document.getElementById('paramsContainer');
        if (this.checked) {
            paramsContainer.style.display = 'block';
        } else {
            paramsContainer.style.display = 'none';
        }
    });
});

// 切换标签页
function switchTab(tabId) {
    // 隐藏所有标签页内容
    const tabPanes = document.querySelectorAll('.tab-pane');
    tabPanes.forEach(pane => pane.classList.remove('active'));
    
    // 移除所有标签的激活状态
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // 显示选中的标签页内容
    document.getElementById(tabId).classList.add('active');
    
    // 激活选中的标签
    event.target.classList.add('active');
}

// 显示消息
function showMessage(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'}"></i> ${message}`;
    
    // 插入到当前活动的标签页顶部
    const activePane = document.querySelector('.tab-pane.active');
    activePane.insertBefore(alertDiv, activePane.firstChild);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 3000);
}

// 显示加载状态
function showLoading(buttonId) {
    const button = document.getElementById(buttonId);
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="loading"></span> 处理中...';
    button.disabled = true;
    return originalText;
}

// 隐藏加载状态
function hideLoading(buttonId, originalText) {
    const button = document.getElementById(buttonId);
    button.innerHTML = originalText;
    button.disabled = false;
}

// 获取访问令牌
async function getToken() {
    const accessKeyId = document.getElementById('accessKeyId').value;
    const accessKeySecret = document.getElementById('accessKeySecret').value;
    
    if (!accessKeyId || !accessKeySecret) {
        showMessage('请填写Access Key ID和Secret', 'danger');
        return;
    }
    
    const originalText = showLoading('startJobBtn');
    
    try {
        const response = await fetch('/api/get_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                accessKeyId: accessKeyId,
                accessKeySecret: accessKeySecret
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('令牌获取成功！', 'success');
        } else {
            showMessage(data.message, 'danger');
        }
    } catch (error) {
        showMessage('网络错误：' + error.message, 'danger');
    } finally {
        hideLoading('startJobBtn', originalText);
    }
}

// 获取应用列表
async function getApplications() {
    try {
        const response = await fetch('/api/get_applications');
        const data = await response.json();
        
        if (data.success) {
            applicationData = data.data['完整信息'];
            const applicationSelect = document.getElementById('applicationSelect');
            applicationSelect.innerHTML = '<option value="">请选择应用</option>';
            
            data.data['应用列表'].forEach((app, index) => {
                const option = document.createElement('option');
                option.value = index;
                option.textContent = app;
                applicationSelect.appendChild(option);
            });
            
            showMessage('应用列表刷新成功！', 'success');
        } else {
            showMessage(data.message, 'danger');
        }
    } catch (error) {
        showMessage('网络错误：' + error.message, 'danger');
    }
}

// 加载机器人参数
async function loadRobotParams() {
    const applicationSelect = document.getElementById('applicationSelect');
    const selectedIndex = applicationSelect.value;
    
    if (!selectedIndex) {
        showMessage('请先选择应用', 'danger');
        return;
    }
    
    const robotUuid = applicationData[selectedIndex].robotUuid;
    
    try {
        const response = await fetch('/api/get_robot_params', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                robotUuid: robotUuid
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayParams(data.inputParams);
            showMessage('参数加载成功！', 'success');
        } else {
            showMessage(data.message, 'danger');
        }
    } catch (error) {
        showMessage('网络错误：' + error.message, 'danger');
    }
}

// 显示参数
function displayParams(params) {
    const paramsList = document.getElementById('paramsList');
    paramsList.innerHTML = '';
    
    if (!params || params.length === 0) {
        paramsList.innerHTML = '<p>该应用没有流程参数</p>';
        return;
    }
    
    params.forEach(param => {
        const paramItem = document.createElement('div');
        paramItem.className = 'param-item';
        
        paramItem.innerHTML = `
            <div class="param-label">${param.name}</div>
            <div class="param-type">${param.type}</div>
            <input type="text" class="form-control" value="${param.value || ''}" data-name="${param.name}" data-type="${param.type}">
        `;
        
        paramsList.appendChild(paramItem);
    });
}

// 获取参数值
function getParamValues() {
    const paramInputs = document.querySelectorAll('#paramsList input');
    const params = [];
    
    paramInputs.forEach(input => {
        const name = input.getAttribute('data-name');
        const type = input.getAttribute('data-type');
        let value = input.value;
        
        // 类型转换
        if (type === 'int') {
            value = parseInt(value) || 0;
        } else if (type === 'float') {
            value = parseFloat(value) || 0.0;
        } else if (type === 'bool') {
            value = value.toLowerCase() === 'true';
        }
        
        params.push({
            name: name,
            value: value,
            type: type
        });
    });
    
    return params;
}

// 启动任务
async function startJob() {
    const accountName = document.getElementById('accountName').value;
    const applicationSelect = document.getElementById('applicationSelect');
    const selectedIndex = applicationSelect.value;
    
    if (!accountName) {
        showMessage('请填写机器人账号', 'danger');
        return;
    }
    
    if (!selectedIndex) {
        showMessage('请选择应用', 'danger');
        return;
    }
    
    const robotUuid = applicationData[selectedIndex].robotUuid;
    const useParams = document.getElementById('useParams').checked;
    let params = null;
    
    if (useParams) {
        params = getParamValues();
    }
    
    const originalText = showLoading('startJobBtn');
    
    try {
        const response = await fetch('/api/start_job', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                robotUuid: robotUuid,
                accountName: accountName,
                params: params
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentJobUuid = data.jobUuid;
            document.getElementById('startJobBtn').disabled = true;
            document.getElementById('stopJobBtn').disabled = false;
            
            showMessage('任务启动成功！', 'success');
            startJobStatusMonitoring();
        } else {
            showMessage(data.message, 'danger');
        }
    } catch (error) {
        showMessage('网络错误：' + error.message, 'danger');
    } finally {
        hideLoading('startJobBtn', originalText);
    }
}

// 停止任务
async function stopJob() {
    if (!currentJobUuid) {
        showMessage('没有正在运行的任务', 'danger');
        return;
    }
    
    try {
        const response = await fetch('/api/stop_job', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                jobUuid: currentJobUuid
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('任务停止成功！', 'success');
            stopJobStatusMonitoring();
        } else {
            showMessage(data.message, 'danger');
        }
    } catch (error) {
        showMessage('网络错误：' + error.message, 'danger');
    }
}

// 开始监控任务状态
function startJobStatusMonitoring() {
    if (jobStatusInterval) {
        clearInterval(jobStatusInterval);
    }
    
    jobStatusInterval = setInterval(async () => {
        if (!currentJobUuid) return;
        
        try {
            const response = await fetch(`/api/job_status/${currentJobUuid}`);
            const data = await response.json();
            
            if (data.success) {
                updateJobStatus(data.data);
                
                if (data.data.status === 'finished' || data.data.status === 'error' || data.data.status === 'stopped') {
                    stopJobStatusMonitoring();
                }
            }
        } catch (error) {
            console.error('获取任务状态失败:', error);
        }
    }, 2000);
}

// 停止监控任务状态
function stopJobStatusMonitoring() {
    if (jobStatusInterval) {
        clearInterval(jobStatusInterval);
        jobStatusInterval = null;
    }
    
    document.getElementById('startJobBtn').disabled = false;
    document.getElementById('stopJobBtn').disabled = true;
    currentJobUuid = null;
}

// 更新任务状态显示
function updateJobStatus(statusData) {
    const statusDiv = document.getElementById('jobStatus');
    const logsDiv = document.getElementById('jobLogs');
    
    // 更新状态徽章
    const statusBadge = `<span class="status-badge status-${statusData.status}">${statusData.status}</span>`;
    statusDiv.innerHTML = `任务状态: ${statusBadge} | 开始时间: ${new Date(statusData.start_time).toLocaleString()}`;
    
    // 更新日志
    if (statusData.logs && statusData.logs.length > 0) {
        logsDiv.innerHTML = '';
        statusData.logs.forEach(log => {
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            logEntry.innerHTML = `
                <span class="log-time">[${log.time}]</span>
                <span class="log-status-${log.status}">${log.message}</span>
            `;
            logsDiv.appendChild(logEntry);
        });
        
        // 滚动到底部
        logsDiv.scrollTop = logsDiv.scrollHeight;
    }
}

// 启动定时任务
async function startSchedule() {
    const scheduleUuid = document.getElementById('scheduleUuid').value;
    const accessKeyId = document.getElementById('accessKeyIdTask').value;
    const accessKeySecret = document.getElementById('accessKeySecretTask').value;
    
    if (!scheduleUuid || !accessKeyId || !accessKeySecret) {
        showMessage('请填写所有必需字段', 'danger');
        return;
    }
    
    const originalText = showLoading('startScheduleBtn');
    
    try {
        const response = await fetch('/api/start_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                scheduleUuid: scheduleUuid,
                accessKeyId: accessKeyId,
                accessKeySecret: accessKeySecret
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentTaskUuid = data.taskUuid;
            document.getElementById('startScheduleBtn').disabled = true;
            document.getElementById('stopScheduleBtn').disabled = false;
            
            showMessage('定时任务启动成功！', 'success');
            startTaskStatusMonitoring();
        } else {
            showMessage(data.message, 'danger');
        }
    } catch (error) {
        showMessage('网络错误：' + error.message, 'danger');
    } finally {
        hideLoading('startScheduleBtn', originalText);
    }
}

// 停止定时任务
async function stopSchedule() {
    if (!currentTaskUuid) {
        showMessage('没有正在运行的定时任务', 'danger');
        return;
    }
    
    const accessKeyId = document.getElementById('accessKeyIdTask').value;
    const accessKeySecret = document.getElementById('accessKeySecretTask').value;
    
    try {
        const response = await fetch('/api/stop_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                taskUuid: currentTaskUuid,
                accessKeyId: accessKeyId,
                accessKeySecret: accessKeySecret
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('定时任务停止成功！', 'success');
            stopTaskStatusMonitoring();
        } else {
            showMessage(data.message, 'danger');
        }
    } catch (error) {
        showMessage('网络错误：' + error.message, 'danger');
    }
}

// 开始监控定时任务状态
function startTaskStatusMonitoring() {
    if (taskStatusInterval) {
        clearInterval(taskStatusInterval);
    }
    
    taskStatusInterval = setInterval(async () => {
        if (!currentTaskUuid) return;
        
        try {
            const response = await fetch(`/api/job_status/${currentTaskUuid}`);
            const data = await response.json();
            
            if (data.success) {
                updateTaskStatus(data.data);
                
                if (data.data.status === 'finished' || data.data.status === 'error' || data.data.status === 'stopped') {
                    stopTaskStatusMonitoring();
                }
            }
        } catch (error) {
            console.error('获取定时任务状态失败:', error);
        }
    }, 2000);
}

// 停止监控定时任务状态
function stopTaskStatusMonitoring() {
    if (taskStatusInterval) {
        clearInterval(taskStatusInterval);
        taskStatusInterval = null;
    }
    
    document.getElementById('startScheduleBtn').disabled = false;
    document.getElementById('stopScheduleBtn').disabled = true;
    currentTaskUuid = null;
}

// 更新定时任务状态显示
function updateTaskStatus(statusData) {
    const statusDiv = document.getElementById('taskStatus');
    const logsDiv = document.getElementById('taskLogs');
    
    // 更新状态徽章
    const statusBadge = `<span class="status-badge status-${statusData.status}">${statusData.status}</span>`;
    statusDiv.innerHTML = `任务状态: ${statusBadge} | 开始时间: ${new Date(statusData.start_time).toLocaleString()}`;
    
    // 更新日志
    if (statusData.logs && statusData.logs.length > 0) {
        logsDiv.innerHTML = '';
        statusData.logs.forEach(log => {
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            logEntry.innerHTML = `
                <span class="log-time">[${log.time}]</span>
                <span class="log-status-${log.status}">${log.message}</span>
            `;
            logsDiv.appendChild(logEntry);
        });
        
        // 滚动到底部
        logsDiv.scrollTop = logsDiv.scrollHeight;
    }
}