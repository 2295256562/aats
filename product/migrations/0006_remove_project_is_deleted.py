# Generated by Django 2.1.14 on 2020-05-27 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_project_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='is_deleted',
        ),
    ]