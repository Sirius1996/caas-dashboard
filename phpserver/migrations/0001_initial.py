# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-29 02:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('code_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('container_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('version', models.FloatField()),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('img_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('repo', models.CharField(max_length=50)),
                ('tag', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=200)),
                ('dockerfile', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('p_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('version', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=200)),
                ('state', models.BooleanField(default=True)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='phpserver.Code')),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='phpserver.Container')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('r_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('u_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('pwd', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='phpserver.Role')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='phpserver.User'),
        ),
        migrations.AddField(
            model_name='container',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='phpserver.Image'),
        ),
    ]
