import ast
import datetime
import json
import logging
import os
import re
import time
import unittest

# from celery.utils.logger import get_task_loggerger

from myCelery.main import app
# from product.models import ApiCase, Headers, Report
from product.models import *
from utils.api.httpServer import httpservice

from requests import Session


@app.task(name="run_test")
def run_test(TaskNo, ids, projectid, address):
    data = []   # 存储函数变量
    c_pass = 0
    c_fail = 0
    start_time = ''

    # 1. 通过接口项目信息获取headers 和 url前缀
    headers = Headers.objects.values().get(project_id=projectid)
    head = json.loads(headers['headers'])
    headersdict = {x['headerSetKey']: x['headersSetValue'] for x in head if x['headersStatus'] == True}
    # print(headersdict)
    # print(type(headersdict))
    print(ids)

    for i in ids:
        try:
            report = Report.objects.get(R_Number=TaskNo)
            report.R_Status = 2
            report.save()
            start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 1. 通过id获取对应接口用例信息
            obj = Case.objects.values().get(pk=i)
            params = json.loads(obj['params'])
            print(params)
            if obj['type'] != 2:
                params = json.loads(obj['params'])
                params = {x['key']: x['value'] for x in params if x['initiate'] == True}
            # 执行测试用例
            # print(data)
            # 替换变量
            sheaders = str(headersdict)
            headersdict = httpservice.extract(sheaders, data)
            # print(headersdict)
            # print(params)
            resp = httpservice(obj['method'], address + obj['url'], obj['type'], params, ast.literal_eval(headersdict))
            respnonse = resp.request()
            print(respnonse.json())
            if respnonse.status_code == 200:
                # logger.logger.info('响应结果:%s' % respnonse.json())
                # logger.logger.info('校验方式:%s' % obj['checkType'])
                # logger.logger.info('校验值%s:' % obj['checkText'])
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

            content = """[ 请求信息 ]</br>URL: {}</br>Headers: {}</br>Body: {}</br>[ 响应信息 ]</br>Status: {}</br>Content: {}""".format(address + obj['url'], headersdict, respnonse.request.body, respnonse.status_code,
                               respnonse.text.encode('utf-8'))
            # print(content)

            CaseReport.objects.create(case_id=i, case_name=obj['case_name'], case_method=obj['method'],
                                       case_url=address + obj['url'],
                                       case_headers=headersdict,
                                       case_params=params, case_response=respnonse.json(), case_expect=obj['checkText'],
                                       case_stauts=check,
                                       case_report=TaskNo, case_log=content)

            # 匹配到$符然后转换
            data.clear()
            data.append(respnonse.json())
        except:
            continue

    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = Report.objects.get(R_Number=TaskNo)
    report.R_CasePass = c_pass
    report.R_CaseFail = c_fail
    report.R_StartTime = start_time
    report.R_EndTime = end_time
    report.R_Status = 3
    report.save()
    return "执行成功"


@app.task(name="getAPi")
def getApi(swagger_url, project_name, productid):
    """
    根据swagger返回的json数据插入数据库
    :param swagger_url:
    :param project_name:
    :return:
    """
    res = Session().request('get', swagger_url).json()
    # 获取解决地址
    data = res.get('paths')
    # 获取接口参数
    definitions = res.get('definitions')

    for k, v in data.items():
        pa_res = re.split(r'[/]+', k)
        dir, *file = pa_res[1:]

        if len(v) > 1:
            v = {'post': v.get('post')}
        for _k, _v in v.items():
            try:
                method = _k
                api = k
                caseName = _v.get('summary')
                data_or_params = 'params' if method == 'get' else 'data'
                parameters = _v.get('parameters')
                if parameters[0]['schema']:
                    schema = parameters[0]['schema']
                    address = schema['$ref']
                    ccc = address.split('/')
                    ddd = definitions[ccc[-1]]
                    parameters = ddd['properties']
                else:
                    parameters = _v.get('parameters')
                tag = _v.get('tags')
            except:
                continue
        # print(api, method, caseName, tag, data_or_params, json.dumps(parameters))
        API.objects.create(api=api, method=method, api_name=caseName, tag=tag, params_type=data_or_params,
                           parameters=json.dumps(parameters), product_id=productid)

    return "执行成功"


@app.task(name="run_case")
def run_case():
    pass
