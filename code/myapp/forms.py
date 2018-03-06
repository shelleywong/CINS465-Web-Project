from django import forms
from django.core.validators import validate_email, validate_slug

def verifySuggestion(value):
    if len(value) < 10:
        raise forms.ValidationError("Not long enough")
    # return the verified data (cleaned or not)
    return value

class Suggestion_Form(forms.Form):
    suggestion = forms.CharField(validators=[verifySuggestion,validate_slug],
        label='Suggestion', max_length=240)
    author = forms.CharField(label='Author',max_length=240)
