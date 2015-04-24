from django.shortcuts import render


def dashboard(request, db_slug):
    context = {'db': db_slug}
    return render(request, 'dashboard.html', context)
