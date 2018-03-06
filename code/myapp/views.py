from django.shortcuts import render
from django.http import HttpResponse

from .models import Suggestion_Model
from .forms import Suggestion_Form

# Create your views here.
def index(request):
    #return HttpResponse("Hello World")
    class_num = 'CINS 465'
    message = 'Hello World'
    example_list = ['one','two','three']
    example_list2 = []
    for i in range(3):
        example_list2 += [i+1]
    context = {
        'class_num':class_num,
        'message':message,
        'example_list':example_list,
        'example_list2':example_list2
    }
    return render(request, 'index.html', context)

def login_view(request):
    class_num = 'CINS 465'
    message = 'Hello World'
    context = {
        'class_num':class_num,
        'message':message,
        }
    return render(request,'login.html', context)

def suggestion_view(request):
    class_num = 'CINS 465'
    message = 'Hello World'
    example_list = ['one','two','three']
    example_list2 = []
    for i in range(3):
        example_list2 += [i+1]

    if request.method == 'POST':
        form = Suggestion_Form(request.POST)
        if form.is_valid():
            suggest = Suggestion_Model(
                suggestion=form.cleaned_data['suggestion'],
                author=form.cleaned_data['author']
            )
            suggest.save()
            form = Suggestion_Form()
    else:
        form = Suggestion_Form()

    suggestion_list = Suggestion_Model.objects.all()

    context = {
        'class_num':class_num,
        'message':message,
        'example_list':example_list,
        'example_list2':example_list2,
        'suggestion_list':suggestion_list,
        'form':form
    }
    return render(request, 'suggestion.html', context)
