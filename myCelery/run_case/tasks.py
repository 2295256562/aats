import ast
import datetime
import json
import logging
import time

# from celery.utils.logger import get_task_loggerger

from myCelery.main import app
# from product.models import ApiCase, Headers, Report
from product.models import *
from utils.api.httpServer import httpservice

# logger = get_task_loggerger(__name__)
logger = logging.getLogger('mdjango')

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
    # print(headersdict)
    # print(type(headersdict))

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
        # print(data)
        # 替换变量
        logger.info('用例ID:%d' % i)
        sheaders = str(headersdict)
        headersdict = httpservice.extract(sheaders, data)
        logger.info('请求方式:%s' % obj['method'])
        logger.info('请求url:%s' % address + obj['url'])
        logger.info('请求headers:%s' % headersdict)
        logger.info('请求参数:%s' % params)

        resp = httpservice(obj['method'], address + obj['url'], obj['type'], params, ast.literal_eval(headersdict))
        respnonse = resp.request()
        if respnonse.status_code == 200:
            logger.info('响应结果:%s' % respnonse.json())
            logger.info('校验方式:%s' % obj['checkType'])
            logger.info('校验值%s:' % obj['checkText'])
            check = resp.checkRequest(obj['checkType'], json.loads(obj['checkText']))
            # case报告详情表中插入数据
            if check == '成功':
                c_pass += 1
            else:
                c_fail += 1
        else:
            # 状态码不等于200, 失败数加1
            c_fail += 1
            check = "失败"

        templates = """[ID]: {} \n[接口]: {}\n[校验方式]: {}\n[校验属性]: {}\n[校验结果]: {}""".format(i, address + obj['url'], obj['checkType'], obj['checkText'], check)

        # checkStauts = respnonse.status_code != 200 && check == '失败'
        APIcaseinfo.objects.create(case_id=i, case_name=obj['case_name'], case_method=obj['method'],
                                   case_url=address + obj['url'],
                                   case_headers=headersdict,
                                   case_params=params, case_response=respnonse.json(), case_expect=obj['checkText'],
                                   case_stauts=check,
                                   case_report=TaskNo, case_log=templates)

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
def add(x, y):
    c = x + y
    print(1111, c)
    return '1111'
