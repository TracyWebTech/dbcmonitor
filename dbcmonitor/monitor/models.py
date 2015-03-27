from django.db import models

# Create your models here.

class Replication(models.Model):
    host_name = models.CharField(max_length=15)
    rep_user = models.CharField(max_length=30)
    log_file = models.CharField(max_length=50)
    log_position = models.IntegerField()

class SlaveReplication(Database):
    master_rep = models.ForeignKey('Replication')

class Comparison(models.Model):
    master_rep = models.ForeignKey('Replication')
    slave_rep = models.ForeignKey('SlaveReplication')


class DatabaseStatus(models.Model):
    replication = models.ForeignKey('Replication')
    db_name = models.CharField(max_length=20)

class TableStatus(models.Model):
    database = models.ForeignKey('Database')
    table_name = models.CharField(max_length=20)
    status = models.CharField(max_length=15)
