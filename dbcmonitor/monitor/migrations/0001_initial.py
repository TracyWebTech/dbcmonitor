# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_name', models.CharField(max_length=15)),
                ('conn_status', models.CharField(max_length=20)),
                ('log_file', models.CharField(max_length=50)),
                ('log_position', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SlaveReplication',
            fields=[
                ('replication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='monitor.Replication')),
                ('master_rep', models.ForeignKey(related_name='master_replication', to='monitor.Replication')),
            ],
            options={
            },
            bases=('monitor.replication',),
        ),
        migrations.CreateModel(
            name='TableStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=15)),
                ('status_date', models.DateTimeField()),
                ('database', models.ForeignKey(to='monitor.DatabaseStatus')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='replication',
            name='organization',
            field=models.ForeignKey(to='monitor.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='databasestatus',
            name='replication',
            field=models.ForeignKey(to='monitor.SlaveReplication'),
            preserve_default=True,
        ),
    ]
