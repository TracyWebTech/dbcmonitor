from django.shortcuts import HttpResponse
from django.http import HttpResponse


# Create your views here.
def home(request):
    html = "<html><body>Monitor Home Page</body></html>" 
    return HttpResponse(html)


def check_replication(request):
    a = compare.delay(3,7)
    html = "<html><body>Monitor Replication Request Page</body></html>" 
    return HttpResponse(html)
