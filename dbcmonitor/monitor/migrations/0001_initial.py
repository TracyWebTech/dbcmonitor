# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                 auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('status_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                 auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('token', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Replication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                 auto_created=True, primary_key=True)),
                ('host_name', models.CharField(max_length=15)),
                ('master_rep', models.ForeignKey(related_name='master',
                 blank=True, to='monitor.Replication', null=True)),
                ('organization', models.ForeignKey(to='monitor.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReplicationStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                 auto_created=True, primary_key=True)),
                ('conn_status', models.CharField(max_length=20)),
                ('status_date', models.DateTimeField()),
                ('log_file', models.CharField(max_length=50)),
                ('log_position', models.IntegerField()),
                ('replication', models.ForeignKey(to='monitor.Replication')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                 auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('last_status', models.CharField(max_length=15)),
                ('database', models.ForeignKey(to='monitor.Database')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TableStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                 auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=15)),
                ('table', models.ForeignKey(to='monitor.Table')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='database',
            name='replication',
            field=models.ForeignKey(to='monitor.Replication'),
            preserve_default=True,
        ),
    ]
