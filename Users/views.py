from django.shortcuts import render
from rest_framework import permissions
from rest_framework.permissions import AllowAny

from Users.serializer import UserRegSerializer
from utils.baseViewSet import BaseViewSet


class RegUserView(BaseViewSet):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = ()
    serializer_class = UserRegSerializer

