from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username' }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'phone_number', 'password1', 'password2',)
