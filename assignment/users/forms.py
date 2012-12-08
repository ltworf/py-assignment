from django import forms

class UserForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    birth_date = forms.DateField()