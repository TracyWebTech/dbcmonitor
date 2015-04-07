from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Replication(models.Model):
    master_rep = models.ForeignKey('self',
                                   related_name='master',
                                   blank=True,
                                   null=True,
                                   )

    organization = models.ForeignKey('Organization')
    host_name = models.CharField(max_length=15)

    def __str__(self):
        return self.host_name


class ReplicationStatus(models.Model):
    replication = models.ForeignKey('Replication')
    conn_status = models.CharField(max_length=20)
    status_date = models.DateTimeField()
    log_file = models.CharField(max_length=50)
    log_position = models.IntegerField()

    def __str__(self):
        return "[{}] {}: {}".format(self.status_date,
                                    self.replication.host_name,
                                    self.conn_status,
                                    )


class Database(models.Model):
    replication = models.ForeignKey('Replication')
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Table(models.Model):
    database = models.ForeignKey('Database')
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class TableStatus(models.Model):
    table = models.ForeignKey('Table')
    status = models.CharField(max_length=15)
    status_date = models.DateTimeField()

    def __str__(self):
        return "[{}] {}: {}".format(self.status_date, self.table, self.status)
