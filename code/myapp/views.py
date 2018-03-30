from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime

from .models import *
from .forms import *

from django.views.decorators.csrf import csrf_exempt

import json
import sys

# Create your views here.
# date format adapted from:
# https://ourcodeworld.com/articles/read/555/how-to-format-datetime-objects-in-the-view-and-template-in-django
def index(request):
    #return HttpResponse("Hello World")
    myDate = datetime.now()
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
        'example_list2':example_list2,
        'date':myDate
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

@csrf_exempt
def suggestion_api(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        try:
            suggest = Suggestion_Model(suggestion=json_data['suggestion'])
            auth = Suggestion_Model(author=json_data['author'])
            suggest.save()
            auth.save()
            return HttpResponse("hello")
        except:
            return HttpResponse("Unexpected error:"+str(sys.exc_info()[0]))
    if request.method == 'PUT':
        json_data = json.loads(request.body)
        try:
            suggest = Suggestion_Model.objects.get(pk=json_data['id'])
            suggest.suggestion = json_data['suggestion']
            suggest.author = json_data['author']
            suggest.save()
            return HttpResponse("hello")
        except:
            return HttpResponse("Unexpected error:"+str(sys.exc_info()[0]))
    if request.method == 'DELETE':
        json_data = json.loads(request.body)
        try:
            suggest = Suggestion_Model.objects.get(pk=json_data['id'])
            suggest.delete()
            return HttpResponse("hello")
        except:
            return HttpResponse("Unexpected error:"+str(sys.exc_info()[0]))
    if request.method == 'GET':
        suggestion_list = Suggestion_Model.objects.all()
        suggestion_dictionary = {}
        suggestion_dictionary["suggestions"] = []
        for suggest in suggestion_list:
            comment_list = Comment_Model.objects.filter(suggestion=suggest)
            comment_json = []
            for comm in comment_list:
                comment_json += [{
                    "comment":comm.comment,
                    "id":comm.id,
                    "created_on":comm.created_on
                }]
            suggestion_dictionary["suggestions"] += [{
                "id":suggest.id,
                "comments":comment_json,
                "suggestion":suggest.suggestion,
                "author":suggest.author,
                "created_on":suggest.created_on
            }]
        print(suggestion_dictionary)
        return JsonResponse(suggestion_dictionary)

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