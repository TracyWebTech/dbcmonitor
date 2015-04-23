from django.shortcuts import render

from replications.models import Replication


def dashboard(request, pk):
    context = {'database_pk': pk}
    return render(request, 'dashboard.html', context)
