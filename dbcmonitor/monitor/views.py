from django.shortcuts import HttpResponse
from django.http import HttpResponse
import json


# Create your views here.
def home(request):
    html = "<html><body>Monitor Home Page</body></html>" 
    return HttpResponse(html)


def check_replication(request):
    html = "<html><body>Monitor Replication Request Page</body></html>" 
    return HttpResponse(html)

def save_replication_status(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

    return HttpResponse()
