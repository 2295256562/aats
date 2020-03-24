import json
import re

import jsonpath as jsonpath
import requests
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


class httpservice:

    def __init__(self, method, url, type, parameters=None, headers={'Content-Type': 'application/json'}):
        self.method = method
        self.url = url
        self.type = type
        self.parameters = parameters
        self.headers = headers

    def checkRequest(self, checkType, checkText):
        """
        :param checkType:  str 校验类型
        :param checkText:  str 校验值
        :return:
        """
        resp = self.request().json()
        check = ''

        # 响应断言
        if checkType == 'text_response':
            log.info('预期值:%s ==== 实际值%s' %(json.loads(checkText, resp)))
            if json.loads(checkText) == resp:
                check = '成功'
                log.info('校验通过')
            else:
                check = '失败'
                log.info('校验失败')

        # jsonpath 断言
        if checkType == 'json_response':
            want = {x['key']: x['value'] for x in checkText}
            key = list(want.keys())
            value = list(want.values())
            # print(want)
            # print(key)
            # print(value)
            for i, j in zip(key, value):
                # print(i)
                # print(resp)
                reslut = self.JsonPath(resp, i)
                # print(type(reslut))
                # print(reslut)
                if isinstance(reslut[0], str):
                    res = " ".join(reslut)
                    # print(res)
                    if res == j:
                        log.info('预期值:%s === 实际值%s' % (res, j))
                        check = '成功'
                        log.info('校验通过')
                    else:
                        check = '失败'
                        log.info('校验失败')
                        return check
                else:
                    if reslut == j:
                        check = '成功'
                    else:
                        check = '失败'
                        return check

        return check

    def request(self):
        global resp

        if self.method == '1':
            if self.type == 1:
                # print(self.url)
                # print(self.parameters)
                # print(self.headers)
                resp = requests.get(url=self.url, params=self.parameters, headers=self.headers, verify=False)

        if self.method == '2':
            if self.type == 1:
                headers = self.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
                resp = requests.post(url=self.url, data=self.parameters, headers=headers)

            if self.type == 2:
                # print(json.loads(self.parameters))
                # print(type(self.parameters))
                resp = requests.post(url=self.url, json=self.parameters, headers=self.headers)
                # print(resp)

            if self.type == 3:
                headers = self.headers.update({'Content-Type': 'multipart/form-data'})
                resp = requests.post(url=self.url, data=self.parameters, headers=headers)

        return resp

    @staticmethod
    def JsonPath(res, expr):
        # 1. 把res转换成json格式
        # respCmtJson = re.sub(r"(,?)(\w+?)\s+?:", r"\1'\2' :", res);
        # respCmtJson = res.replace("'", "\"").replace("True", "true").replace("None", "null").replace("False", "false")
        # s1 = str(res)
        # res_json = json.loads(res)
        expr = expr.replace("'", "\"")
        results = jsonpath.jsonpath(res, expr)
        return results

    @classmethod
    def common_check(cls, resp):
        """
        公共Check方法，检查 200 响应码和 msg字段值（'success'）
        :param resp:
        :return:
        """
        assert resp.status_code == 200, cls.error_request_datail(resp, '响应码非200')

    @classmethod
    def error_request_datail(cls, resp, error_msg=''):
        """
         打印完整请求信息，用于报错时调试
        :param resp: request.response 对象
        :param error_msg:  错误信息
        :return: 请求信息（字符串
        """
        content = '{}\n{}'.format(cls._get_request_info(resp), error_msg)
        return content

    @staticmethod
    def _get_request_info(resp):
        """
        从 request.response 对象中提取请求和返回的详细信息
        :param resp: request.response 对象
        :return: 请求信息（字符串）
        """
        content = """
                    [ 请求信息 ]
                    URL: {}
                    Headers: {}
                    Body: {}
                    ------------------------
                    [ 响应信息 ]
                    Status: {}
                    Content: {}
                    """.format(resp.request.url, resp.request.headers, resp.request.body, resp.status_code,
                               resp.text)
        return content

    @staticmethod
    def extract(string, dict):
        try:
            while re.search('\$\{(.*?)\}', string):
                    key = re.search('\$\{(.*?)\}', string).group(0)
                    value = re.search('\$\{(.*?)\}', string).group(1)
                    n = value.split('.')
                    # print(n)
                    tmp = dict[0][n[0]]
                    string = string.replace(key, str(tmp))
        except:
            string = string
        return string

dict =[{'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTgzOTEzNTQ5LCJlbWFpbCI6IjIyOTUyNTY1NjJAcXEuY29tIn0.zHtZddZqij2OtShKsCUfYfUob5kmaO5H7w9SpP_oOoY', 'id': 1, 'username': 'admin'}]


if __name__ == '__main__':
    cc = {'Content-Type': 'application/json', 'Authorization': '${token}'}

    print(httpservice.extract(str(cc), dict))
