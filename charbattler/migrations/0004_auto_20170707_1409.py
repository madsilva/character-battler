# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 19:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('charbattler', '0003_auto_20170706_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('post_datetime', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='matchup',
            name='char1_wins',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='matchup',
            name='char2_wins',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='matchup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charbattler.Matchup'),
        ),
    ]
