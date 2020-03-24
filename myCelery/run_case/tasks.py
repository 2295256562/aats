import datetime
import json
import logging
import time

from celery.utils.log import get_task_logger

from myCelery.main import app
# from product.models import ApiCase, Headers, Report
from product.models import *
from utils.api.httpServer import httpservice


log = get_task_logger(__name__)

# @app.task(name='run_test')
# def run_test(x,y):
#     c = x+y
#     return c

@app.task(name="run_test")
def run_test(TaskNo, ids, projectid, address):
    data = []
    c_pass = 0
    c_fail = 0
    start_time = ''

    # 1. 通过接口项目信息获取headers 和 url前缀
    headers = Headers.objects.values().get(project_id=projectid)
    head = json.loads(headers['headers'])
    headersdict = {x['headerSetKey']: x['headersSetValue'] for x in head if x['headersStatus'] == True}

    for i in ids:
        report = Report.objects.get(R_Number=TaskNo)
        report.R_Status = 2
        report.save()
        start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 1. 通过id获取对应接口用例信息
        obj = ApiCase.objects.values().get(pk=i)
        params = json.loads(obj['params'])
        if obj['type'] != 2:
            params = json.loads(obj['params'])
            params = {x['key']: x['value'] for x in params if x['initiate'] == True}
        # 执行测试用例
        print(data)
        # 替换变量
        log.info('用例ID:%d' % i)
        headersdict = httpservice.extract(str(headersdict), data)
        log.info('请求方式:%s' % obj['method'])
        log.info('请求url:%s' % address + obj['url'])
        log.info('请求参数:%s' % params)
        resp = httpservice(obj['method'], address + obj['url'], obj['type'], params, eval(headersdict))
        respnonse = resp.request()
        if respnonse.status_code == 200:
            log.info('响应结果:%s' % respnonse.json())
            log.info('校验方式:%s' % obj['checkType'])
            log.info('校验值%s:' % obj['checkText'])
            check = resp.checkRequest(obj['checkType'], json.loads(obj['checkText']))
            if check == '成功':
                c_pass += 1
            else:
                c_fail += 1
        else:
            # 状态码不等于200, 失败数加1
            c_fail += 1

        # 匹配到$符然后转换
        data.clear()
        data.append(respnonse.json())
    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = Report.objects.get(R_Number=TaskNo)
    report.R_CasePass = c_pass
    report.R_CaseFail = c_fail
    report.R_StartTime = start_time
    report.R_EndTime = end_time
    report.R_Status = 3
    report.save()
    return "执行成功"


@app.task(name="time_task")
def Timetask(ids):
    pass

@app.task(name='add')
def add(x,y):
    c = x+y
    print(1111, c)
    return '1111'