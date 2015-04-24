
from django import template
from django.http import Http404

from ..models import Replication

register = template.Library()


@register.inclusion_tag('replications/templatetags/status_table.html')
def status_table(db):
    status_table = Replication.objects.status_table(db)
    if not status_table:
        raise Http404("No replications found for '{}'".format(db))

    return {'status_table': status_table}
