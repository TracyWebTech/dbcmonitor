from django.db import models

class Replication(models.Model):
    host_name = models.CharField(max_length=15)
    conn_status = models.CharField(max_length=20)
    log_file = models.CharField(max_length=50)
    log_position = models.IntegerField()

    def __str__(self):
        return self.host_name


class SlaveReplication(Replication):
    master_rep = models.ForeignKey('Replication',
            related_name='master_replication')

    def __str__(self):
        return self.host_name


class DatabaseStatus(models.Model):
    replication = models.ForeignKey('SlaveReplication')
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class TableStatus(models.Model):
    database = models.ForeignKey('DatabaseStatus')
    name = models.CharField(max_length=20)
    status = models.CharField(max_length=15)
    status_date = models.DateTimeField()

    def __str__(self):
        return self.name
