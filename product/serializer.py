import json

from rest_framework import serializers
from .models import *


class AddProjectSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Project
        fields = '__all__'  # 返回所有字段


class HeadersSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Headers
        fields = '__all__'  # 返回所有字段

    def to_representation(self, instance):
        data = super().to_representation(instance)
        headers = json.loads(data['headers'])
        data['headers'] = {x['headerSetKey']: x['headersSetValue'] for x in headers}
        data['headers'] = str(data['headers'])
        # 返回处理之后的数据
        return data


class HeadersInfoSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Headers
        fields = '__all__'  # 返回所有字段

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['headers'] = json.loads(data['headers'])
        # data['headers'] = {x['headerSetKey']: x['headersSetValue'] for x in headers }
        # data['headers'] = str(data['headers'])
        # 返回处理之后的数据
        return data


class ListProjectSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'  # 返回所有字段

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project_address'] = json.loads(data['project_address'])
        # 返回处理之后的数据
        return data


class SoureceProjectSer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_name', 'id']


class AddModelSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Model
        fields = '__all__'  # 返回所有字段


class ListModelSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # project_name = serializers.CharField(source='project_id.project_name')
    project_name = serializers.CharField(source='project_id.project_name')

    # project_name = serializers.ReadOnlyField()
    # model_name = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Model
        fields = '__all__'


class modelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'model_name']


class addAPicaseSer(serializers.ModelSerializer):
    create_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ApiCase
        fields = '__all__'


class listApiCase(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    project_name = serializers.CharField(source='project_id.project_name')

    class Meta:
        model = ApiCase
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['params'] = str(json.loads(data['params']))
        # 返回处理之后的数据
        return data




class GETinfoSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    project_name = serializers.CharField(source='project_id.project_name')

    class Meta:
        model = ApiCase
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['params'] = json.loads(data['params'])
        data['checkText'] = json.loads(data['checkText'])
        # 返回处理之后的数据
        return data


class reportinfoSer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)


    class Meta:
        model = Report
        fields = '__all__'


from djcelery.models import CrontabSchedule, PeriodicTask

class timeTaskSer(serializers.ModelSerializer):
    date_changed = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = PeriodicTask
        fields = '__all__'