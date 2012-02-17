from django import forms

class CreateUser(forms.Form):
    email = forms.EmailField(label="Their Email")
    name = forms.CharField(label="Name")
    message = forms.CharField(label="Body", widget=forms.Textarea)
