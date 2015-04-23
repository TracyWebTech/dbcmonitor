
from django import template

from ..models import Replication

register = template.Library()


@register.inclusion_tag('replications/templatetags/status_table.html',
                        takes_context=True)
def status_table(context):
    return {'status_table': Replication.objects.status_table(
        context['database_pk'])
    }
