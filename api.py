"""
写在前面：
    该文件存放调用api接口的代码
    例如影刀开放的api调度接口等等......
"""

import json
import requests

# 请求方法
method = ['GET', 'POST']


def callApi(url, data, headers=None, method=None):
    """
    调用接口返回json数据(字典)
    """
    if method == 'GET':
        result = requests.get(url=url, data=data, headers=headers).json()
        return result
    elif method == 'POST':
        result = requests.post(url=url, data=data, headers=headers).json()
        return result


def getAccessToken(accessKeyId, accessKeySecret):
    """
    获取accessToken
    :return:accessToken
    """
    accessToken =  None
    try:
        response = callApi(
            urls['getAccessToken'].format(accessKeyId, accessKeySecret),
            None, {'Content-Type': 'application/x-www-form-urlencoded'}, method[0])
        print(response)
        accessToken = response['data']['accessToken']
        print('已获取accessToken：{}'.format(accessToken))
        print('-----------------------帅气的分割线-------------------------')
        return accessToken

    except Exception as e:
        print(e)
        "e = 'data'"
        return e


def query_application(accessToken,param):  # 获取应用列表
    url = "https://api.yingdao.com/oapi/robot/v2/query"
    headers = {
        "Authorization": f"Bearer {accessToken}"
    }
    # data = callApi(url, None, headers, method[0])
    data = requests.get(url=url, headers=headers,params=param).json()
    data_list = [{"账号名称": i["ownerName"], "应用名称": i["robotName"], "robotUuid": i["robotUuid"]} for i in data["data"]]
    print(data_list)
    return data_list


def queryAllApplication(accessToken):  # 获取所有应用
    data_list = []
    for i in range(1,5):#默认查50页应用列表(每页50个)
        params = {
            "page":i,
            "size":50
        }
        data_list += query_application(accessToken,params)
    yy_list = [x['应用名称'] for x in data_list]
    return {'完整信息': data_list, '应用列表': yy_list}


def startJob(accessToken, robotUuid, accountName,param=None):
    """
    启动任务，并返回jobUuid
    :return:jobUuid
    """
    nan = ''
    if param != None:
        nan = json.dumps({
            "accountName": accountName,
            "robotUuid": robotUuid,
            "params": param
        })
    else:
        nan = json.dumps({
            "accountName": accountName,
            "robotUuid": robotUuid
        })
    headers = {'Content-Type': 'application/json', 'authorization': 'Bearer {}'.format(accessToken)}
    # data = callApi(urls['startJob'], data, headers, method[1])
    data = requests.post(url=urls['startJob'], headers=headers, data=nan).json()
    print(data)
    jobUuid = data['data']['jobUuid']
    print('已获取jobUuid：' + jobUuid)
    print('-----------------------帅气的分割线-------------------------')
    return jobUuid


def job_stop(accessToken, jobUuid):
    url = "https://api.yingdao.com/oapi/dispatch/v2/job/stop"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "jobUuid": jobUuid
    })
    re_data = callApi(url, data, headers, method[1])
    return re_data

def taskStop(accessToken, taskUuid):
    url = "https://api.yingdao.com/oapi/dispatch/v2/task/stop"
    headers = {
        "Authorization": f"Bearer {accessToken}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "taskUuid": taskUuid
    })
    re_data = callApi(url, data, headers, method[1])
    return re_data


def query(accessToken, jobUuid):
    """
    查询应用启动结果
    :return:
    """
    data = json.dumps({
        "jobUuid": jobUuid,
    })
    headers = {'Content-Type': 'application/json', 'authorization': 'Bearer {}'.format(accessToken)}
    return callApi(
        urls['query'],
        data,
        headers,
        method[1])['data']['status']
def query_RobotParam(accessToken, robotUuid): #查询应用结构
    '''
    :param accessToken: 鉴权
    :param robotUuid: 应用uuid
    :return: 输入参数，输出参数
    '''
    url = "https://api.yingdao.com/oapi/robot/v2/queryRobotParam?robotUuid={}".format(robotUuid)
    headers = {
        "Authorization":f"Bearer {accessToken}"
    }
    data = {
        "robotUuid":robotUuid
    }
    data = callApi(url,headers=headers, data= None, method=method[0])
    # print(data)
    # 判断是否含有输入输出参数
    if len(data["data"])!=0:
        if len(data["data"]["inputParams"])!=0 and len(data["data"]["outputParams"])!=0:
            return data["data"]["inputParams"],data["data"]["outputParams"]#查询应用结构
        elif len(data["data"]["inputParams"])!=0 and len(data["data"]["outputParams"])==0:
            return data["data"]["inputParams"],None#查询应用结构
        elif len(data["data"]["inputParams"])==0 and len(data["data"]["outputParams"])!=0:
            return None,data["data"]["outputParams"]#查询应用结构
    else:
        return None,None

def queryJobStatus(accessToken, taskUuid):
    """
    查询应用启动结果
    :return:
    """
    url = 'https://api.yingdao.com/oapi/dispatch/v2/task/query'
    data = json.dumps({
        "taskUuid": taskUuid,
    })
    headers = {'Content-Type': 'application/json', 'authorization': 'Bearer {}'.format(accessToken)}
    return callApi(
        url,
        data,
        headers,
        method[1])['data']['status']

def startScheduleUuid(accessToken, scheduleUuid):
    url = 'https://api.winrobot360.com/oapi/dispatch/v2/task/start'
    data = json.dumps({
        "scheduleUuid": scheduleUuid
    })
    headers = {'Content-Type': 'application/json', 'authorization': 'Bearer {}'.format(accessToken)}
    # taskUuid = callApi(url, data, headers, method[1])['data']['taskUuid']

    taskUuid1 = callApi(url, data, headers, method[1])
    print(taskUuid1)
    taskUuid = taskUuid1['data']['taskUuid']


    print('已获取taskUuid：' + taskUuid)
    print('-----------------------帅气的分割线-------------------------')
    return taskUuid



# 调用的接口网址
urls = {
    'getAccessToken': 'https://api.yingdao.com/oapi/token/v2/token/create?accessKeyId={}&accessKeySecret={}',
    'startJob': 'https://api.yingdao.com/oapi/dispatch/v2/job/start',
    'query': 'https://api.yingdao.com/oapi/dispatch/v2/job/query'
}

# todo -------------------------改变调度相关信息和应用入参即可------------------------------------------
# 调度相关信息
informationOfDispatch = {
    'accessKeyId': '8cYQWNPby6TVwr3Z@platform',
    'accessKeySecret': 'r7wYtmApyEB8HCXgMvhPJ0bZcfN4kzaK',
    "accountName": "admin@fckjgz",
    "robotUuid": "13842197-a729-46a8-973e-abef125e837c",
    "scheduleUuid": "12091614-6a0b-401f-9fa7-cb97b6271609",
    'comment': '伯符的调度相关信息',
}

# 应用入参
informationOfrobot = [
    {"name": "parameter1",
     "value": '啊杰连锁火锅店',
     "type": "str"
     },
    {"name": "parameter2",
     "value": '直播卖拖鞋',
     "type": "str"
     }]

if __name__ == '__main__':
    token = getAccessToken('SNf63XdyraPDxUZc@platform', 'fmd91tTMSp5Y4RNkC2yuEcW0r8vVqAzn')
    # taskUuid = startScheduleUuid(token, 'b526203f-0279-42e4-b2d5-55813c3eb556')
    # print(token)
    # print(taskUuid)
    # response = queryJobStatus(token, taskUuid)
    res = queryAllApplication(token)
    print(res)
    # {'code': 400, 'success': False, 'requestId': 'ffc20e6f1c88c673bf47283b', 'serverInstName': 'xybot-dispatch',
    #  'msg': '参数错误，未查询到任务'}
    # print(response)
    yy = '啊杰火锅店调度应用'
    uuid = [x for x in res['完整信息'] if x['应用名称'] ==  '啊杰火锅店调度应用'][0]['robotUuid']
    print(uuid)
    canshu = query_RobotParam(token,uuid)
    print(canshu[0])
    print(canshu[1])
    print(type(canshu))