from django import forms
from django.core.validators import validate_email, validate_slug
from django.core.validators import MinValueValidator, MaxValueValidator

def verifySuggestion(value):
    if len(value) < 10:
        raise forms.ValidationError("Not long enough")
    # return the verified data (cleaned or not)
    return value

class Suggestion_Form(forms.Form):
    suggestion = forms.CharField(validators=[verifySuggestion,validate_slug],
        label='Suggestion', max_length=240)
    author = forms.CharField(label='Author',max_length=240)

class Book_Form(forms.Form):
    title = forms.CharField(label='Title', max_length=255)
    blurb = forms.CharField(widget=forms.Textarea,label='Blurb')
    num_pages = forms.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(1000000)],label="Number of Pages")
    price = forms.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)],label="Price")
    available = forms.BooleanField(label="Available")
