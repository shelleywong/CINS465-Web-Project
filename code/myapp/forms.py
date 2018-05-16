from django import forms
from django.forms import DateTimeField
from django.core.validators import validate_email, validate_slug
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import *

# from in-class practice form
def verifySuggestion(value):
    if len(value) < 1:
        raise forms.ValidationError("Not long enough")
    return value

class Join_Group_Form(forms.Form):
    group = forms.CharField(label="Group",max_length=240)

class Post_Form(forms.Form):
    subject = forms.CharField(
        validators=[verifySuggestion],
        label='Subject',
        max_length=240)
    details = forms.CharField(widget=forms.Textarea,label='Post')

class Post_Comment_Form(forms.Form):
    comment = forms.CharField(widget=forms.Textarea,label='Comment')

    def save(self,post_id,req_user,commit=True):
        original_post = Post_Model.objects.get(pk=post_id)
        comm = Post_Comment_Model(
            comment=self.cleaned_data["comment"],
            post_topic = original_post,
            author=req_user
        )
        if commit:
            comm.save()
        return comm

class Login_Form(AuthenticationForm):
    username = forms.CharField(
        label = "Username",
        max_length = 32,
        widget = forms.TextInput(attrs={'name':'username'})
    )
    password = forms.CharField(
        label = "Password",
        max_length = 32,
        widget = forms.PasswordInput()
    )

class Registration_Form(UserCreationForm):
    first_name = forms.CharField(
        label = "First Name",
        max_length = 32,
        required = True
    )
    last_name = forms.CharField(
        label = "Last Name",
        max_length = 32,
        required = True
    )
    email = forms.EmailField(
        label = "Email",
        required = True
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(Registration_Form,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class Student_Reg_Form(forms.ModelForm):
    class Meta:
        model = Student_Model
        exclude = ['user']

class Edit_Profile_Form(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )

class Edit_Student_Profile(forms.ModelForm):
    class Meta:
        model = Student_Model
        exclude = ['user']

#in-class practice forms
class Suggestion_Form(forms.Form):
    suggestion = forms.CharField(validators=[verifySuggestion],
        label='Suggestion', max_length=240)

class Comment_Form(forms.Form):
    comment = forms.CharField(
        label='Comment',
        max_length=240
    )
    def save(self,sugg_id,req_user,commit=True):
        sugg = Suggestion_Model.objects.get(pk=sugg_id)
        comm = Comment_Model(
            comment = self.cleaned_data['comment'],
            suggestion = sugg
        )
        if commit:
            comm.save()
        return comm

#practice form
class Book_Form(forms.Form):
    title = forms.CharField(label='Title', max_length=255)
    blurb = forms.CharField(widget=forms.Textarea,label='Blurb')
    num_pages = forms.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(1000000)],label="Number of Pages")
    price = forms.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)],label="Price")
    available = forms.BooleanField(label="Available")
