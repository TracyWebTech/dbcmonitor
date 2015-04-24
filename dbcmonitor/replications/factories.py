
import random
import string

import factory

from django.utils import timezone

from factory import fuzzy

from .models import Replication

NOW = timezone.now()
START_DATE = NOW - timezone.timedelta(weeks=4)

DATABASE_NAMES = ['CWKS', 'BusProject', 'Xavier', 'Bloom']

HOSTNAMES = [
    'mysql-a.example.com',
    'mysql-b.example.com',
    'mysql-c.example.com',
    'mysql-d.example.com',
    'mysql-e.example.com',
    'mysql-f.example.com',
    'mysql-g.example.com',
]

STATUS = [0, 1, 99]


def get_slave(obj):
    hosts = [host for host in HOSTNAMES if not host == obj.master]
    return random.choice(hosts)


class ReplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'replications.Replication'

    database = fuzzy.FuzzyChoice(DATABASE_NAMES)
    master = fuzzy.FuzzyChoice(HOSTNAMES)
    slave = factory.LazyAttribute(get_slave)


def get_sent_time(obj):
    delay = random.randint(10**3, 10**7)
    return obj.received_time - timezone.timedelta(microseconds=delay)


def get_replication(obj):
    return Replication.objects.order_by('?').first()


class ReplicationStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'replications.ReplicationStatus'

    replication = factory.LazyAttribute(get_replication)
    status = fuzzy.FuzzyChoice(STATUS)
    log_file = fuzzy.FuzzyText(length=6, chars=string.digits,
                               prefix='mysql-bin.')
    log_position = fuzzy.FuzzyInteger(1000000, 999999999)
    received_time = fuzzy.FuzzyDateTime(START_DATE, NOW)
    sent_time = factory.LazyAttribute(get_sent_time)
