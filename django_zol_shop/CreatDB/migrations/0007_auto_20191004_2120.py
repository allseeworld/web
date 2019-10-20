# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-10-04 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CreatDB', '0006_auto_20191004_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopinfo',
            name='shop_list_id',
            field=models.CharField(default='', max_length=256, verbose_name='列表商品id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shoplist',
            name='big_id',
            field=models.CharField(default='', max_length=256, verbose_name='大类id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shoplist',
            name='small_id',
            field=models.CharField(default='', max_length=256, verbose_name='小类id'),
            preserve_default=False,
        ),
    ]