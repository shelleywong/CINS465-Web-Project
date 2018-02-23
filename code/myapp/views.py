from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #return HttpResponse("Hello World")
    class_num = 'CINS 465'
    message = 'Hello World'
    example_list = ['one','two','three']
    #for i in range(3):
        #example_list+=[i+1]
    context = {
        'class_num':class_num,
        'message':message,
        'example_list':example_list
    }
    return render(request, 'index.html', context)
        #{'class_num':class_num, 'message':message})
