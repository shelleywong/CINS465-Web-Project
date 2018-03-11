from django.shortcuts import render
from django.http import HttpResponse

from .models import Suggestion_Model
from .models import Book
from .forms import Suggestion_Form
from .forms import Book_Form

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

def book_view(request):
    class_num = 'CINS 465'
    message = 'Hello World'
    example_list = ['one','two','three']
    example_list2 = []
    for i in range(3):
        example_list2 += [i+1]

    if request.method == 'POST':
        form = Book_Form(request.POST)
        if form.is_valid():
            books = Book(
                title = form.cleaned_data['title'],
                blurb = form.cleaned_data['blurb'],
                num_pages = form.cleaned_data['num_pages'],
                price = form.cleaned_data['price'],
                available = form.cleaned_data['available']
            )
            books.save()
            form = Book_Form()
    else:
        form = Book_Form()

    book_list = Book.objects.all()

    context = {
        'class_num':class_num,
        'message':message,
        'example_list':example_list,
        'example_list2':example_list2,
        'book_list':book_list,
        'form':form
    }
    return render(request, 'book.html', context)
