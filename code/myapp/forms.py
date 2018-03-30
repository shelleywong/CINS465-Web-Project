from django import forms
from django.forms import DateTimeField
from django.core.validators import validate_email, validate_slug
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

def verifySuggestion(value):
    if len(value) < 10:
        raise forms.ValidationError("Not long enough")
    # return the verified data (cleaned or not)
    return value

class Suggestion_Form(forms.Form):
    suggestion = forms.CharField(validators=[verifySuggestion,validate_slug],
        label='Suggestion', max_length=240)
    author = forms.CharField(label='Author',max_length=240)
    #created_on = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M:%S'])

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
    email = forms.EmailField(
        label = "Email",
        required = True
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(registration_form,self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class Book_Form(forms.Form):
    title = forms.CharField(label='Title', max_length=255)
    blurb = forms.CharField(widget=forms.Textarea,label='Blurb')
    num_pages = forms.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(1000000)],label="Number of Pages")
    price = forms.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)],label="Price")
    available = forms.BooleanField(label="Available")
