from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    moblie = models.CharField(max_length=11, verbose_name="手机号", unique=True)
    avatar = models.ImageField(upload_to="avatar", verbose_name="头像", null=True, blank=True, help_text="图像图片")

    class Meta:
        db_table = 'user'
        verbose_name = "用户表"
        verbose_name_plural = verbose_name