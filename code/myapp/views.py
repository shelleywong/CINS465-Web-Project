from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserChangeForm


from .models import *
from .forms import *

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import json
import sys

# Create your views here.
# date format adapted from:
# https://ourcodeworld.com/articles/read/555/how-to-format-datetime-objects-in-the-view-and-template-in-django
def index(request):
    #return HttpResponse("Hello World")
    myDate = datetime.now()
    site_name = 'homeroom'
    message = """Simple to use. No cost to you.
        A safe place to connect with your class and communicate better."""
    post_list = Post_Model.objects.all()
    student_list = Student_Model.objects.all()
    context = {
        'site_name':site_name,
        'message':message,
        'post_list':post_list,
        'student_list':student_list,
        'date':myDate
    }
    return render(request, 'index.html', context)

def about_view(request):
    return render(request, 'about.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        user_form = Registration_Form(request.POST)
        student_form = Student_Reg_Form(request.POST,request.FILES)
        if all((user_form.is_valid(), student_form.is_valid())):
            user_profile = user_form.save()
            student_profile = student_form.save(commit=False)
            student_profile.user = user_profile
            student_profile.save()
            return redirect('/login/')
    else:
        user_form = Registration_Form(request.POST)
        student_form = Student_Reg_Form(request.POST,request.FILES)

    context = {
        'user_form': user_form,
        'student_form': student_form
    }
    return render(request,"registration/register.html",context)

# def login(request):
#     class_num = 'CINS 465'
#     message = 'Hello World'
#     context = {
#         'class_num':class_num,
#         'message':message,
#         }
#     return render(request,'login.html', context)

def logout(request):
    logout(request)
    return render(request,"index.html")

@login_required(login_url='/login/')
def profile_view(request):
    logged_in_user = request.user
    if request.method == 'POST':
        user_form = Registration_Form(request.POST)
        student_form = Student_Reg_Form(request.POST,request.FILES)
        if all((user_form.is_valid(), student_form.is_valid())):
            student = Student_Model(
                about=form.cleaned_data['about'],
                image=form.cleaned_data['image'],
                image_description=form.cleaned_data['image_description']
            )
            student.save()
            return redirect("/")
    else:
        user_form = Registration_Form(request.POST)
        student_form = Student_Reg_Form(request.POST,request.FILES)

    # users = User.objects.all().select_related('student_model')
    u = User.objects.get(username=request.user)
    about_student = u.student_model.about
    student_image = u.student_model.image
    img_desc = u.student_model.image_description
    # student = Student_Model.objects.get(User,pk=logged_in_user.id)
    # student.interests = 'Going on adventures'
    # student.save()

    student_list = Student_Model.objects.all()
    # for student in student_list:
    #     if student.id == logged_in_user.id:
    #         current_student = student
    context = {
        'student_list':student_list,
        'user_form':user_form,
        'student_form':student_form,
        'about_student':about_student,
        'student_image':student_image,
        'img_desc':img_desc
        # 'users':users,
        # 'students':students
    }
    return render(request, 'profile.html', context)
    # if request.method == 'POST':
    #     user_form = Registration_Form(request.POST,request.FILES)
    #     student_form = Student_Reg_Form(request.POST,request.FILES)
    #     if user_form.is_valid() and student_form.is_valid():
    #         user_form.save()
    #         student_form.save()
    #         return redirect('profile.html')
    # else:
    #     user_form = Registration_Form()
    #     student_form = Student_Reg_Form()
    # context = {
    #     'user_form': user_form,
    #     'student_form': student_form
    # }
    # return render(request,"profile.html",context)
    # student_list = Student_Model.objects.all()
    # context = {
    #     "student_list":student_list
    # }
    # return render(request,"profile.html",context)

# adapted from: https://www.youtube.com/watch?v=JmaxoPBvp1M
@login_required(login_url='/login/')
def edit_profile_view(request):
    if request.method == 'POST':
        form = Edit_Profile_Form(request.POST, instance=request.user)
        #form2 = Edit_Profile2(request.POST)
        if form.is_valid(): # or form2.is_valid():
            form.save()
            #form2.save()
            return redirect('/profile/')
    else:
        form = Edit_Profile_Form(instance=request.user)
        #form2 = Edit_Profile2(request.POST)

        context = {
            "form":form
        #    "form2":form2
        }
        return render(request,"edit_profile.html",context)

@login_required(login_url='/login/')
def forum_view(request):
    myDate = datetime.now()
    if request.method == 'POST':
        form = Post_Form(request.POST)
        if form.is_valid():
            forum_post = Post_Model(
                subject=form.cleaned_data['subject'],
                details=form.cleaned_data['details'],
                author=request.user
            )
            forum_post.save()
            return redirect("/")
            #form = Post_Form()
    else:
        form = Post_Form()

    post_list = Post_Model.objects.all()
    context = {
        'post_list':post_list,
        'form':form,
        'date':myDate
    }
    return render(request, 'forum.html', context)

@csrf_exempt
def forum_api(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        try:
            a_post = Post_Model(subject=json_data['subject'],details=json_data['details'])
            a_post.save()
            return HttpResponse("hello")
        except:
            return HttpResponse("Unexpected error:"+str(sys.exc_info()[0]))
    if request.method == 'PUT':
        json_data = json.loads(request.body)
        try:
            a_post = Post_Model.objects.get(pk=json_data['id'])
            a_post.subject = json_data['subject']
            a_post.details = json_data['details']
            a_post.save()
            return HttpResponse("hello")
        except:
            return HttpResponse("Unexpected error:"+str(sys.exc_info()[0]))
    if request.method == 'DELETE':
        json_data = json.loads(request.body)
        try:
            a_post = Post_Model.objects.get(pk=json_data['id'])
            a_post.delete()
            return HttpResponse("hello")
        except:
            return HttpResponse("Unexpected error:"+str(sys.exc_info()[0]))
    if request.method == 'GET':
        post_list = Post_Model.objects.all()
        post_dictionary = {}
        post_dictionary["posts"] = []
        for post_item in post_list:
            comment_list = Post_Comment_Model.objects.filter(post_topic_id=post_item)
            comment_json = []
            for comm in comment_list:
                comment_json += [{
                    "comment":comm.comment,
                    "id":comm.id,
                    "author":comm.author.username,
                    "created_on":comm.created_on.strftime('%m/%d/%Y %H:%M')
                }]
            post_dictionary["posts"] += [{
                "id":post_item.id,
                "subject":post_item.subject,
                "details":post_item.details,
                "comments":comment_json,
                "author":post_item.author.username,
                "created_on":post_item.created_on.strftime('%m/%d/%Y %H:%M')
            }]
        print(post_dictionary)
        return JsonResponse(post_dictionary)

@login_required(login_url='/login/')
def comment_view(request,post_topic_id):
    if request.method == 'POST':
        post_comm = Post_Comment_Form(request.POST)
        if post_comm.is_valid():
            post_comm.save(post_topic_id, request.user)
            return redirect("/")
    else:
        post_comm = Post_Comment_Form
    post_list = Post_Model.objects.all()
    comment_list = Post_Comment_Model.objects.all()
    context={
        "post_comm":post_comm,
        "post_topic_id":post_topic_id,
        "post_list":post_list,
        "comment_list":comment_list
    }
    return render(request,'comment.html',context)


@login_required(login_url='/login/')
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
                suggestion=form.cleaned_data['suggestion']
                #author=request.user
            )
            suggest.save()
            form = Suggestion_Form()
    else:
        form = Suggestion_Form()

    # if request.method == 'GET':
    #     form = Suggestion_Form(request.GET)
    #     if form.is_valid():
    #         print(request.GET['author'])
    #         print(request.POST['author'])
    # else:
    #     form = Suggestion_Form()

    #a = Suggestion_Model(suggestion='aSuggestion',author='aAuthor')
    #a.save()

    #b = Comment_Model(comment='comment_to_a',created_on=datetime.now(),suggestion=a)
    #a.save()

    # c = Suggestion_Model(suggestion='cSuggestion',author='cAuthor')
    # c.save()
    #
    # c.author = 'CAuthor'
    # c.save()

    # d = Suggestion_Model(id=22,created_on=datetime.now())
    # d.author='author22'
    # d.save()
    #
    # e = Suggestion_Model(id=24,created_on=datetime.now())
    # e.author='author24'
    # e.suggestion='suggestion24'
    # e.save()
    #
    # Suggestion_Model(id=23).delete()
    #Suggestion_Model(id=29,suggestion='aSuggestion',author='aAuthor').delete()
    # for i in range(33,39):
    #     Suggestion_Model(id=i).delete()


    #f = Comment_Model(comment='comment_to_3',created_on=datetime.now(),suggestion=Suggestion_Model(id=3))
    #f.save()

    # Suggestion_Model(id=22).author = 'author22'
    # Suggestion_Model(id=22).created_on = datetime.now()
    # Suggestion_Model(id=22).save()

    #Suggestion_Model.objects.filter(author__contains='author')




    # Suggestion_Model.objects.get(id=1)
    # Suggestion_Model.objects.get(author__startswith='awesome')
    # Suggestion_Model.objects.get(author__contains='author')


    # if request.method == 'DELETE':
    #     form = Suggestion_Form(request.POST)
    #     if form.is_valid():
    #         instance = Suggestion_Model.objects.get(
    #             pk=form.cleaned_data['id'],
    #         )
    #         instance.delete()
    #         form = Suggestion_Form()
    # else:
    #     form = Suggestion_Form()

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
            suggest.save()
            return HttpResponse("hello")
        except:
            return HttpResponse("Unexpected error:"+str(sys.exc_info()[0]))
    if request.method == 'PUT':
        json_data = json.loads(request.body)
        try:
            suggest = Suggestion_Model.objects.get(pk=json_data['id'])
            suggest.suggestion = json_data['suggestion']
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
                    "id":comm.id
                    # "created_on":comm.created_on
                }]
            suggestion_dictionary["suggestions"] += [{
                "id":suggest.id,
                "comments":comment_json,
                "suggestion":suggest.suggestion
                # "created_on":suggest.created_on.strftime('%m/%d/%Y %H:%M')
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
