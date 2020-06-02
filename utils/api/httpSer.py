import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aats.settings")
django.setup()
import copy
import re
import jsonpath
import requests
from loguru import logger
from testify import assert_equal

from product.models import Case, API


class HttpService:
    """
    http request请求类
    """
    userdata = []

    def __init__(self, ):
        self.msge = []

    def regx(self, string, userdata):
        """
        正则提取方法
        :param string: 传入提取需要提取的参数 语法为 ${}
        :param userdata: 全局userdata变量
        :return: 替换后的字符串
        """
        try:
            if isinstance(string, dict):
                string = str(string)
            while re.search( '\$\{(.*?)\}', string):
                logger.info(f"替换前：{string}")
                self.msge.append(f"替换前：{string}")
                key = re.search('\$\{(.*?)\}', string).group(0)
                value = re.search('\$\{(.*?)\}', string).group(1)
                logger.info(f"变量表达式：{value}")
                self.msge.append(f"变量表达式：{value}")
                for i, v in enumerate(userdata):
                    try:
                        tmp = v[value]
                        string = string.replace(key, str(tmp))
                    except:
                        continue
                    logger.info("{0} 替换 {1}".format(value, tmp))
                    self.msge.append("{0} 替换 {1}".format(value, tmp))
                    logger.info(f"替换后：{string}")
                    self.msge.append(f"替换后：{string}")
        except:
            string = string

        return string

    def request(self, method, url, params=None, data=None, json=None,
                headers={"content-type": "application/json"}):
        """
        请求方法
        :param method: 请求方法
        :param url: 请求url
        :param params: params参数
        :param data: data参数
        :param json: json类型参数
        :param headers: 请求头
        :return: 返回self对象
        """
        self.msge.clear()
        url = self.regx(url, self.userdata)
        logger.info(f"请求url：{url}")
        self.msge.append(f"请求url：{url}")
        params = self.regx(params or data or json, self.userdata)
        logger.info(f"请求参数：{params or data or json}")
        self.msge.append(f"请求参数：{params or data or json}")
        headers = self.regx(headers, self.userdata)

        if method is "get":
            self.response = requests.request(method=method, url=url, params=params, headers=eval(headers), verify=False)
        elif method is "post" and data is not None:
            self.response = requests.request(method=method, url=url, data=eval(params), headers=eval(headers),
                                             verify=False)
        else:
            self.response = requests.request(method=method, url=url, json=eval(params), headers=eval(headers),
                                             verify=False)

        logger.info(f"请求头：{self.response.request.headers}")
        self.msge.append(f"请求头：{self.response.request.headers}")
        logger.info(f"响应结果：{self.response.text}")
        self.msge.append(f"响应结果：{self.response.text}")
        logger.info(f"请求耗时：{(self.response.elapsed.microseconds) / 1000}ms")
        self.msge.append(f"请求耗时：{(self.response.elapsed.microseconds) / 1000}ms")
        return self

    def extract(self, extr):
        """
        提取变量
        :param extr: 提示表达式 [{},{}]
        :return:
        """
        value = self.response.json()
        logger.info(f"**** 开始提取变量 *****")
        self.msge.append(f"**** 开始提取变量 *****")
        for _, v in enumerate(extr):
            try:
                key, = v
                logger.info(f"正在进行参数提取：表达式为：{v[key]}")
                self.msge.append(f"正在进行参数提取：表达式为：{v[key]}")
                restul = jsonpath.jsonpath(value, v[key])[0]
                logger.info(f"取到参数对应值为：{restul}")
                self.msge.append(f"取到参数对应值为：{restul}")
                self.userdata.append({key: restul})
            except:
                logger.error("提取失败,表达式可能有误")
                self.msge.append("提取失败,表达式可能有误")
        return self

    def validate(self, expected_value):
        """
        校验返回值字段
        :param expected_value: 校验列表
        :return: 返回校验记录 list
        """
        result = []
        stauts = True
        template = {
            "check_result": "pass",
            "check_value": "",
            "check_type": "",
            "expect": "",
            "result": ""
        }
        # 拿到response
        resp = self.response.json()
        logger.info(f"***** 开始断言判断 *****")
        self.msge.append(f"***** 开始断言判断 *****")
        for i, el in enumerate(expected_value):
            if el['check'] == "status_code":
                assert_equal(self.response.status_code, el['expect'])
                logger.info(f"status_code断言  预期结果：{self.response.status_code} = 实际结果：{el['expect']}")
                logger.info(f"校验结果：pass")
                self.msge.append(f"status_code断言  预期结果：{self.response.status_code} = 实际结果：{el['expect']}")
                self.msge.append(f"校验结果：pass")
                template = copy.deepcopy(template)
                template['check_result'] = "pass"
                template['check_value'] = el['check']
                template['check_type'] = el['comparator']
                template['expect'] = el['expect']
                template['result'] = self.response.status_code
                result.append(template)
            else:
                try:
                    temp = jsonpath.jsonpath(resp, el['check'])[0]
                    if el['comparator'] == "=":
                        try:
                            assert_equal(temp, el["expect"])
                            logger.info(f"jsonpath断言 预期结果：{el['expect']} = 实际结果：{temp}")
                            self.msge.append(f"jsonpath断言  预期结果：{el['expect']} = 实际结果：{temp}")
                            logger.info(f"校验结果：pass")
                            self.msge.append(f"校验结果：pass")
                            template = copy.deepcopy(template)
                            template['check_value'] = el['check']
                            template['check_type'] = el['comparator']
                            template['expect'] = el['expect']
                            template['result'] = temp
                            result.append(template)
                        except  AssertionError as AS:
                            logger.info(f"jsonpath断言  预期结果：{el['expect']}  实际结果：{temp}")
                            self.msge.append(f"jsonpath断言  预期结果：{el['expect']}  实际结果：{temp}")
                            logger.info(f"校验结果：fail")
                            self.msge.append(f"校验结果：faill")
                            template = copy.deepcopy(template)
                            template['check_result'] = "fail"
                            template['check_value'] = el['check']
                            template['check_type'] = el['comparator']
                            template['expect'] = el['expect']
                            template['result'] = temp
                            result.append(template)
                except:
                    logger.error(f"jsonpath没有提取到{el['check']}")
                    logger.error("校验结果：fail")
                    self.msge.append(f"jsonpath没有提取到{el['check']}")
                    self.msge.append("校验结果：fail")

        # 判断result中check_result是否有存在为fail的,如果存在case状态久违false,没有就为true
        for i, va in enumerate(result):
            if va["check_result"] == "fail":
                stauts = False

        return result, stauts

    @classmethod
    def common_check(cls, resp):
        """
        公共Check方法，检查 200 响应码和 msg字段值（'success'）
        :param resp:
        :return:
        """
        assert resp.status_code == 200, cls.error_request_datail(resp, '响应码非200')
        # assert resp.json()['msg'] == 'success', cls.error_request_datail(resp, '响应内容中 msg 不为success')

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

    def msg(self):
        """
        :return: 返回日志list
        """
        return self.msge


def runcase(project_id, header, case_id, report_id):
    """
    :param project_id: 项目id  int
    :param header: 请求headers  dict
    :param case_id: 用例id list
    :param report_id: 测试报告id  int
    :return:
    """
    req = HttpService()
    # 遍历case_id执行用例
    for i in case_id:
        # 通过id查询 case信息
        data = Case.objects.get(pk=i)
        # req.request()
        print(data.__dict__)
        api = API.objects.filter(pk=data.case_api_id)
        print(api.values('api', 'method', 'params_type'))


runcase(1,2,[1],4)
