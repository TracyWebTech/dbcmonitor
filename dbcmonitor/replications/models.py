from django.db import models
from django.utils.translation import ugettext_lazy as _

from organizations.models import Organization

from .managers import ReplicationManager


class Replication(models.Model):
    organization = models.ForeignKey(Organization)
    database = models.CharField(max_length=64)
    master = models.CharField(max_length=255)
    slave = models.CharField(max_length=255)

    def __str__(self):
        return '{} ({} -> {})'.format(self.database, self.master, self.slave)

    objects = ReplicationManager()


class ReplicationStatus(models.Model):

    STATUS_OK = 0
    STATUS_CONFLICT = 1
    STATUS_UNKNOWN = 99

    OK = [STATUS_OK]
    WARN = [STATUS_UNKNOWN]
    ERROR = [STATUS_CONFLICT]

    STATUS_CHOICES = (
        (STATUS_OK, 'OK'),
        (STATUS_CONFLICT, 'Conflict'),
        (STATUS_UNKNOWN, 'Unknown Error'),
    )

    replication = models.ForeignKey(Replication, related_name='status')

    status = models.IntegerField(choices=STATUS_CHOICES)
    log_file = models.CharField(max_length=50)
    log_position = models.IntegerField()
    received_time = models.DateTimeField(auto_now=True)
    sent_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = _('Replication Status')
        get_latest_by = 'sent_time'

    def css_class(self):
        if int(self.status) in self.OK:
            return 'alert-success'

        elif int(self.status) in self.WARN:
            return 'alert-warning'

        elif int(self.status) in self.ERROR:
            return 'alert-danger'

        return ''


class ReplicationError(models.Model):

    replication = models.ForeignKey(ReplicationStatus)

    table = models.CharField(max_length=64)
    code = models.IntegerField()
    message = models.CharField(max_length=255)
