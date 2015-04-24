from django.shortcuts import render, get_object_or_404

from replications.models import Database


def dashboard(request, db_slug):
    context = {'db': get_object_or_404(Database, slug=db_slug)}
    return render(request, 'dashboard.html', context)
