from django import forms

class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=155)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=155)
    password = forms.CharField(widget=forms.PasswordInput)
