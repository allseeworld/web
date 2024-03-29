# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-10-06 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop_Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_name', models.CharField(max_length=64, verbose_name='展示区的名字')),
                ('type_id1', models.IntegerField(verbose_name='商品大类id1')),
                ('type_id2', models.IntegerField(verbose_name='商品大类id2')),
                ('type_id3', models.IntegerField(verbose_name='商品大类id3')),
                ('shop_id1', models.IntegerField(verbose_name='商品id1')),
                ('shop_id2', models.IntegerField(verbose_name='商品id2')),
                ('shop_id3', models.IntegerField(verbose_name='商品id3')),
                ('shop_id4', models.IntegerField(verbose_name='商品id4')),
                ('shop_id5', models.IntegerField(verbose_name='商品id5')),
                ('shop_id6', models.IntegerField(verbose_name='商品id6')),
                ('shop_id7', models.IntegerField(verbose_name='商品id7')),
                ('shop_id8', models.IntegerField(verbose_name='商品id8')),
                ('shop_id9', models.IntegerField(verbose_name='商品id9')),
            ],
            options={
                'verbose_name': '商品展示列表',
                'verbose_name_plural': '商品展示列表',
            },
        ),
    ]
