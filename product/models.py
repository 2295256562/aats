from django.contrib.auth.models import AbstractUser

from utils.Model_obj import SoftDeletableModel
from django.db import models


class Project(SoftDeletableModel):
    # 项目表
    project_name = models.CharField(max_length=64, verbose_name="项目名称")
    project_address = models.CharField(max_length=1024, verbose_name='项目地址')

    class Meta:
        db_table = "project"
        verbose_name = "项目表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project_name


class Model(SoftDeletableModel):
    # 模块表
    model_name = models.CharField(max_length=64, verbose_name='模块名称')
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name='项目id')

    # model_desc = models.CharField(max_length=1024, verbose_name='模块描述')

    class Meta:
        db_table = "model"
        verbose_name = "模块表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.model_name


class ApiCase(SoftDeletableModel):
    # 接口自动化用例表
    case_name = models.CharField(max_length=128, verbose_name="用例名称")
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name="所属项目id")
    model = models.CharField(max_length=64, verbose_name="所属模块")
    method = models.CharField(max_length=2, verbose_name="请求方式")
    url = models.CharField(max_length=1024, verbose_name="接口地址")
    type = models.IntegerField(verbose_name="参数类型")
    params = models.TextField(verbose_name="请求参数")
    checkType = models.CharField(max_length=32, verbose_name="校验类型")
    checkText = models.TextField(verbose_name="校验值")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "apicase"
        verbose_name = "接口用例表"
        verbose_name_plural = verbose_name


class Headers(SoftDeletableModel):
    headers = models.TextField(verbose_name='请求头', blank=True, null=True)
    project_name = models.CharField(max_length=64, verbose_name='项目名称')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目')

    class Meta:
        db_table = "headers"
        verbose_name = "项目表"
        verbose_name_plural = verbose_name


class Report(SoftDeletableModel):
    # 接口测试报告表

    TASK_STATUS = (
        (1, "未开始"),
        (2, "进行中"),
        (3, "已完成"),
    )

    TASK_TYPE = (
        (1, "即时任务"),
        (2, "定时任务")
    )

    R_Number = models.CharField(max_length=64, blank=False, verbose_name='任务编号')
    R_Env = models.CharField(max_length=128, verbose_name='执行环境')
    R_project = models.CharField(max_length=10, verbose_name='所属项目')
    R_CaseId = models.CharField(max_length=1024, verbose_name="报告用例id")
    R_Status = models.IntegerField(default=1, choices=TASK_STATUS, verbose_name='任务状态')
    R_CaseSum = models.IntegerField(verbose_name='任务用例个数')
    R_CasePass = models.IntegerField(verbose_name='成功数', null=True, blank=True)
    R_CaseFail = models.IntegerField(verbose_name='失败数', null=True, blank=True)
    R_StartTime = models.CharField(max_length=200, verbose_name='任务起始时间', null=True, blank=True)
    R_EndTime = models.CharField(max_length=200, verbose_name='任务结束时间', null=True, blank=True)
    R_Type  = models.IntegerField(default=2,choices=TASK_TYPE, verbose_name="任务类型")

    class Meta:
        db_table = "report"
        verbose_name = "接口报告表"
        verbose_name_plural = verbose_name

class ApiILog(SoftDeletableModel):
    caseId = models.IntegerField(verbose_name='用例id')
    caseUrl = models.TextField(verbose_name='接口url')









