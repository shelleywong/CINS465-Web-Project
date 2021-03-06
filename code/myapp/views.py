from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import Group

from .models import *
from .forms import *

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic.edit import UpdateView
from django.utils.safestring import mark_safe
from django.core import serializers
from django.db.models import Q

from random import shuffle, sample
import random

import json
import sys

# Create your views here.
# date format adapted from:
# https://ourcodeworld.com/articles/read/555/how-to-format-datetime-objects-in-the-view-and-template-in-django
def index(request):
    myDate = datetime.now()
    site_name = 'homeroom'
    message = """Simple to use. No cost to you.
        A safe place to connect with your class and communicate better."""
    post_list = Post_Model.objects.all().order_by("-created_on")
    user_list = User.objects.all()
    student_list = Student_Model.objects.all()

    context = {
        'site_name':site_name,
        'message':message,
        'post_list':post_list,
        'student_list':student_list,
        'user_list':user_list,
        'date':myDate
    }
    return render(request, 'index.html', context)

#adapted from: https://djangobook.com/django-forms/
def search_view(request):
    site_name = 'homeroom'
    post_list = Post_Model.objects.all().order_by("-created_on")
    error = False
    search = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            search = True
            searched_posts = Post_Model.objects.filter(
                Q(subject__icontains=q) |
                Q(details__icontains=q)
            )
            context = {
                'search':search,
                'site_name':site_name,
                'post_list':post_list,
                'searched_posts':searched_posts,
                'query': q
            }
            return render(request, 'index.html', context)
    return render(request, 'index.html', {'error':error})

def about_view(request):
    return render(request, 'about.html')

# adapted from: https://stackoverflow.com/questions/27832076/modelform-with-onetoonefield-in-django?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
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

def logout(request):
    logout(request)
    return render(request,"index.html")

# adding a user to a group - adapted from:
#https://stackoverflow.com/questions/6288661/adding-a-user-to-a-group-in-django
#https://stackoverflow.com/questions/4789021/in-django-how-do-i-check-if-a-user-is-in-a-certain-group?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
@login_required(login_url='/login/')
def profile_view(request):
    error = False
    message = ""
    if request.method == "POST":
        form = Join_Group_Form(request.POST)
        if form.is_valid():
            # form.save()
            grp = form.cleaned_data['group']
            group_list = Group.objects.all()
            for g in group_list:
                if grp == g.name and grp != 'professors':
                    current_user = User.objects.get(username = request.user)
                    # my_group = Group.objects.get(name='cins465students')
                    my_group = Group.objects.get(name=grp)
                    current_user.groups.add(my_group)
                    # form.save()
                    return redirect('/')
                else:
                    error = True
                    message = ("The group '" + grp +
                                "' does not currently exist or "
                                "you do not have permission to join."
                                )
    else:
        form = Join_Group_Form()

    student = False
    professor = False
    # group_exists = request.user.groups.filter(name="cins465students").exists()
    if request.user.groups.filter(name="cins465students").exists():
        student = True
    if request.user.groups.filter(name="professors").exists():
        professor = True
    # my_groups = request.user.groups.values_list('name',flat=True)
    student_grp = Group.objects.get(name='cins465students')
    prof_grp = Group.objects.get(name='professors')
    # profs = User.objects.filter(groups__name='cins465students')
    context = {
        # 'my_groups':my_groups,
        'student':student,
        'professor':professor,
        'student_grp':student_grp,
        'prof_grp':prof_grp,
        'error':error,
        'message':message,
        'form':form,
        'user':request.user
    }
    return render(request, 'profile.html', context)

#Reference: 1 (see: CINS465-Shelley-Wong, README.md)
@login_required(login_url='/login/')
def edit_profile_view(request):
    if request.method == 'POST':
        form = Edit_Profile_Form(request.POST, instance=request.user)
        form2 = Edit_Student_Profile(request.POST,request.FILES,instance=request.user)
        if all((form.is_valid(), form2.is_valid())):
            form.save()
            form2.save(commit=False)
            student = Student_Model.objects.get(user=request.user)
            student.about=form2.cleaned_data['about']
            student.image=form2.cleaned_data['image']
            student.image_description=form2.cleaned_data['image_description']
            student.save()
            return redirect('/profile/')
    else:
        form = Edit_Profile_Form(instance = request.user)
        form2 = Edit_Student_Profile(instance=request.user)

    context = {
        "form": form,
        "form2":form2
    }
    return render(request,"edit_profile.html",context)

# adapted from: https://docs.djangoproject.com/en/2.0/topics/auth/default/ and
# https://www.youtube.com/watch?v=QxGKTvx-Vvg&list=PLw02n0FEB3E3VSHjyYMcFadtQORvl1Ssj&index=20
@login_required(login_url='/login/')
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile/')
        else:
            return redirect('/password/')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        'form':form
    }
    return render(request,"password.html",context)

@login_required(login_url='/login/')
def message_board_view(request):
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
    else:
        form = Post_Form()

    post_list = Post_Model.objects.all().order_by("-created_on")
    context = {
        'post_list':post_list,
        'form':form,
        'date':myDate
    }
    return render(request, 'message_board.html', context)

@csrf_exempt
def message_board_api(request):
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
        post_list = Post_Model.objects.all().order_by("-created_on")
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
    myDate = datetime.now()
    if request.method == 'POST':
        post_comm = Post_Comment_Form(request.POST)
        if post_comm.is_valid():
            post_comm.save(post_topic_id, request.user)
            return redirect("/")
    else:
        post_comm = Post_Comment_Form()
    post_list = Post_Model.objects.all()
    comment_list = Post_Comment_Model.objects.all()
    context={
        "date": myDate,
        "post_comm":post_comm,
        "post_topic_id":post_topic_id,
        "post_list":post_list,
        "comment_list":comment_list
    }
    return render(request,'comment.html',context)

@login_required(login_url='/login/')
def meet_view(request):
    return render(request,'people/meet.html')

@login_required(login_url='/login/')
def roster_view(request):
    last_names = User.objects.all().order_by('last_name')
    first_names = User.objects.all().order_by('first_name')
    usernames = User.objects.all().order_by('username')
    student_list = Student_Model.objects.all()
    profs = User.objects.filter(groups__name='professors')
    context = {
        'profs':profs,
        'last_names':last_names,
        'first_names':first_names,
        'usernames':usernames,
        'student_list':student_list
    }
    return render(request,'people/roster.html',context)

@login_required(login_url='/login/')
def person_view(request,this_user):
    current_user = User.objects.get(username = this_user)
    context = {
        # 'room_name_json': mark_safe(json.dumps(room_name)),
        'current_user':current_user
    }
    return render(request, 'group/person.html', context)

@login_required(login_url='/login/')
def face_match_view(request):
    # adapted from: https://stackoverflow.com/questions/976882/shuffling-a-list-of-objects
    # users = User.objects.filter(groups__name='cins465students')
    users = User.objects.all()
    u_list = list(users)
    n = len(u_list)
    user_list = random.sample(u_list,n)
    student_list = Student_Model.objects.all()
    context = {
        # 'users':users,
        # 'n':n,
        'user_list': user_list,
        'student_list':student_list
    }
    return render(request,'people/face_match.html',context)

@csrf_exempt
def students_api(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        try:
            a_user = list(User.objects.all(), fields=('username','first_name','last_name'))
            a_student = list(Student_Model.objects.all(), fields=('user','image'))
            a_user.save()
            a_student.save()
            return HttpResponse(data, mimetype='application/json')
        except:
            return HttpResponse("Unexpected error:"+str(sys.exc_info()[0]))
    if request.method == 'GET':
        # users = User.objects.all()
        users = User.objects.filter(
            groups__name='cins465students').exclude(
            groups__name='professors')
        u_list = list(users)
        n = len(u_list)
        user_queryset = random.sample(u_list,n)
        user_dictionary = {}
        user_dictionary["users"] = []
        for user_item in user_queryset:
            student_item = Student_Model.objects.get(user=user_item)
            user_dictionary["users"] += [{
                'username': user_item.username,
                'first_name': user_item.first_name,
                'last_name': user_item.last_name,
                'image':str(student_item.image)
            }]
        return JsonResponse(user_dictionary, safe=False)

# Reference: 2 (see: CINS465-Shelley-Wong, README.md)
# Reference: 3 (see: CINS465-Shelley-Wong, README.md)
@login_required(login_url='/login/')
def chatroom(request):
    # We want to show the last 10 messages, ordered most-recent-last
    chat_queryset = Chat_Model.objects.order_by("-created_on")[:25]
    chat_message_count = len(chat_queryset)
    if chat_message_count > 0:
        first_message_id = chat_queryset[len(chat_queryset)-1].id
    else:
        first_message_id = -1
    previous_id = -1
    if first_message_id != -1:
        try:
            previous_id = Chat_Model.objects.filter(
                pk__lt=first_message_id).order_by(
                "-pk")[:1][0].id
        except IndexError:
            previous_id = -1
    chat_messages = reversed(chat_queryset)
    most_recent = chat_queryset[0]
    u = User.objects.get(username=request.user)
    current_user = u.first_name
    user_list = User.objects.all()
    student_list = Student_Model.objects.all()
    context = {
        'most_recent':most_recent,
        'chat_messages': chat_messages,
        'first_message_id' : previous_id,
        'current_user':mark_safe(json.dumps(current_user)),
        'user_list':user_list,
        'student_list':student_list
    }
    return render(request, "chat/chatroom.html",context)

# in-class practice view
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

# in-class practice view
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
                }]
            suggestion_dictionary["suggestions"] += [{
                "id":suggest.id,
                "comments":comment_json,
                "suggestion":suggest.suggestion
            }]
        print(suggestion_dictionary)
        return JsonResponse(suggestion_dictionary)

#practice view
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

# Reference: 2 (see: CINS465-Shelley-Wong, README.md) - Practice Chat Room
@login_required(login_url='/login/')
def room(request,room_name):
    name = room_name
    context = {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'name':name
    }
    return render(request, 'chat/room.html', context)
