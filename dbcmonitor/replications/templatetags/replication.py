
from django import template

from ..models import Replication

register = template.Library()


@register.inclusion_tag('replications/templatetags/status_table.html')
def status_table():
    return {'status_table': Replication.objects.status_table()}
