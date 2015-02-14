# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('nickname', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('privilege', models.IntegerField(default=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
