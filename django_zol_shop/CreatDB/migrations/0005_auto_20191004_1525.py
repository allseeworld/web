# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-10-04 07:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CreatDB', '0004_shoplist'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopinfo',
            name='image_url',
            field=models.URLField(default='', verbose_name='图片地址'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shoplist',
            name='image_url',
            field=models.URLField(default='', verbose_name='图片地址'),
            preserve_default=False,
        ),
    ]
