# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, session
import api
import json
import threading
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 请更改为安全的密钥

# 全局变量存储任务状态
task_status = {}
running_jobs = {}

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/api/get_token', methods=['POST'])
def get_token():
    """获取访问令牌"""
    try:
        data = request.get_json()
        access_key_id = data.get('accessKeyId')
        access_key_secret = data.get('accessKeySecret')
        
        token = api.getAccessToken(access_key_id, access_key_secret)
        
        if isinstance(token, str) and token != "'data'":
            session['access_token'] = token
            return jsonify({
                'success': True,
                'message': '令牌获取成功',
                'token': token
            })
        else:
            return jsonify({
                'success': False,
                'message': '令牌获取失败，请检查ID和Secret是否正确'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取令牌时发生错误: {str(e)}'
        })

@app.route('/api/get_applications', methods=['GET'])
def get_applications():
    """获取应用列表"""
    try:
        access_token = session.get('access_token')
        if not access_token:
            return jsonify({
                'success': False,
                'message': '请先获取访问令牌'
            })
        
        data = api.queryAllApplication(access_token)
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取应用列表时发生错误: {str(e)}'
        })

@app.route('/api/get_robot_params', methods=['POST'])
def get_robot_params():
    """获取机器人参数"""
    try:
        data = request.get_json()
        robot_uuid = data.get('robotUuid')
        access_token = session.get('access_token')
        
        if not access_token:
            return jsonify({
                'success': False,
                'message': '请先获取访问令牌'
            })
        
        params = api.query_RobotParam(access_token, robot_uuid)
        
        return jsonify({
            'success': True,
            'inputParams': params[0] if params[0] else [],
            'outputParams': params[1] if params[1] else []
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取机器人参数时发生错误: {str(e)}'
        })

@app.route('/api/start_job', methods=['POST'])
def start_job():
    """启动任务"""
    try:
        data = request.get_json()
        robot_uuid = data.get('robotUuid')
        account_name = data.get('accountName')
        params = data.get('params', None)
        access_token = session.get('access_token')
        
        if not access_token:
            return jsonify({
                'success': False,
                'message': '请先获取访问令牌'
            })
        
        job_uuid = api.startJob(access_token, robot_uuid, account_name, params)
        
        # 启动监控线程
        monitor_thread = threading.Thread(
            target=monitor_job_status,
            args=(access_token, job_uuid)
        )
        monitor_thread.daemon = True
        monitor_thread.start()
        
        running_jobs[job_uuid] = {
            'status': 'running',
            'start_time': datetime.now().isoformat(),
            'logs': []
        }
        
        return jsonify({
            'success': True,
            'jobUuid': job_uuid,
            'message': '任务启动成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'启动任务时发生错误: {str(e)}'
        })

@app.route('/api/stop_job', methods=['POST'])
def stop_job():
    """停止任务"""
    try:
        data = request.get_json()
        job_uuid = data.get('jobUuid')
        access_token = session.get('access_token')
        
        if not access_token:
            return jsonify({
                'success': False,
                'message': '请先获取访问令牌'
            })
        
        result = api.job_stop(access_token, job_uuid)
        
        if result.get('success'):
            if job_uuid in running_jobs:
                running_jobs[job_uuid]['status'] = 'stopped'
            return jsonify({
                'success': True,
                'message': '任务停止成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '任务停止失败'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'停止任务时发生错误: {str(e)}'
        })

@app.route('/api/job_status/<job_uuid>', methods=['GET'])
def get_job_status(job_uuid):
    """获取任务状态"""
    if job_uuid in running_jobs:
        return jsonify({
            'success': True,
            'data': running_jobs[job_uuid]
        })
    else:
        return jsonify({
            'success': False,
            'message': '任务不存在'
        })

@app.route('/api/start_schedule', methods=['POST'])
def start_schedule():
    """启动定时任务"""
    try:
        data = request.get_json()
        schedule_uuid = data.get('scheduleUuid')
        access_key_id = data.get('accessKeyId')
        access_key_secret = data.get('accessKeySecret')
        
        # 获取令牌
        access_token = api.getAccessToken(access_key_id, access_key_secret)
        
        if not isinstance(access_token, str) or access_token == "'data'":
            return jsonify({
                'success': False,
                'message': '令牌获取失败，请检查ID和Secret是否正确'
            })
        
        task_uuid = api.startScheduleUuid(access_token, schedule_uuid)
        
        # 启动监控线程
        monitor_thread = threading.Thread(
            target=monitor_task_status,
            args=(access_token, task_uuid)
        )
        monitor_thread.daemon = True
        monitor_thread.start()
        
        running_jobs[task_uuid] = {
            'status': 'running',
            'start_time': datetime.now().isoformat(),
            'logs': [],
            'type': 'schedule'
        }
        
        return jsonify({
            'success': True,
            'taskUuid': task_uuid,
            'message': '定时任务启动成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'启动定时任务时发生错误: {str(e)}'
        })

@app.route('/api/stop_schedule', methods=['POST'])
def stop_schedule():
    """停止定时任务"""
    try:
        data = request.get_json()
        task_uuid = data.get('taskUuid')
        access_key_id = data.get('accessKeyId')
        access_key_secret = data.get('accessKeySecret')
        
        # 获取令牌
        access_token = api.getAccessToken(access_key_id, access_key_secret)
        
        if not isinstance(access_token, str) or access_token == "'data'":
            return jsonify({
                'success': False,
                'message': '令牌获取失败，请检查ID和Secret是否正确'
            })
        
        result = api.taskStop(access_token, task_uuid)
        
        if result.get('success'):
            if task_uuid in running_jobs:
                running_jobs[task_uuid]['status'] = 'stopped'
            return jsonify({
                'success': True,
                'message': '定时任务停止成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '定时任务停止失败'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'停止定时任务时发生错误: {str(e)}'
        })

def monitor_job_status(access_token, job_uuid):
    """监控任务状态"""
    while job_uuid in running_jobs and running_jobs[job_uuid]['status'] == 'running':
        try:
            status = api.query(access_token, job_uuid)
            current_time = datetime.now().strftime('%H:%M:%S')
            
            log_entry = {
                'time': current_time,
                'status': status,
                'message': f'任务状态: {status}'
            }
            
            running_jobs[job_uuid]['logs'].append(log_entry)
            
            if status == 'finish':
                running_jobs[job_uuid]['status'] = 'finished'
                running_jobs[job_uuid]['logs'].append({
                    'time': current_time,
                    'status': 'finished',
                    'message': '任务执行完成'
                })
                break
            elif status == 'error':
                running_jobs[job_uuid]['status'] = 'error'
                running_jobs[job_uuid]['logs'].append({
                    'time': current_time,
                    'status': 'error',
                    'message': '任务执行出错'
                })
                break
            
            time.sleep(2)
        except Exception as e:
            running_jobs[job_uuid]['logs'].append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'status': 'error',
                'message': f'监控出错: {str(e)}'
            })
            break

def monitor_task_status(access_token, task_uuid):
    """监控定时任务状态"""
    while task_uuid in running_jobs and running_jobs[task_uuid]['status'] == 'running':
        try:
            status = api.queryJobStatus(access_token, task_uuid)
            current_time = datetime.now().strftime('%H:%M:%S')
            
            log_entry = {
                'time': current_time,
                'status': status,
                'message': f'定时任务状态: {status}'
            }
            
            running_jobs[task_uuid]['logs'].append(log_entry)
            
            if status == 'finish':
                running_jobs[task_uuid]['status'] = 'finished'
                running_jobs[task_uuid]['logs'].append({
                    'time': current_time,
                    'status': 'finished',
                    'message': '定时任务执行完成'
                })
                break
            elif status == 'error':
                running_jobs[task_uuid]['status'] = 'error'
                running_jobs[task_uuid]['logs'].append({
                    'time': current_time,
                    'status': 'error',
                    'message': '定时任务执行出错'
                })
                break
            
            time.sleep(2)
        except Exception as e:
            running_jobs[task_uuid]['logs'].append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'status': 'error',
                'message': f'监控出错: {str(e)}'
            })
            break

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)