#!/usr/bin/env python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbcmonitor.settings")

import sys
sys.path.append('dbcmonitor')

import django
django.setup()

from django.contrib.auth.models import User
from organizations.models import Organization
from replications.models import Replication
from replications.factories import ReplicationFactory, ReplicationStatusFactory


def create_data():

    user, created = User.objects.get_or_create(username='admin', defaults={
        'email': 'admin@example.com',
        'is_active': True,
        'is_staff': True,
        'is_superuser': True,
    })
    if created:
        user.set_password('admin')
        user.save()

    try:
        org = Organization.objects.latest('id')
    except Organization.DoesNotExist:
        org = Organization.objects.create(name='Tracy Web Technologies')

    try:
        ReplicationFactory.create_batch(15, organization=org)
    except django.db.utils.IntegrityError:
        pass

    for replica in Replication.objects.all():
        ReplicationStatusFactory(replication=replica)

if __name__ == '__main__':
    create_data()
