from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #return HttpResponse("Hello World")
    class_num = 'CINS 465'
    message = 'Hello World'
    return render(request, 'index.html',
        {'class_num':class_num, 'message':message})
