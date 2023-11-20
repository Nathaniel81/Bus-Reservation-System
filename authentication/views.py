from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import SignUpForm, LoginForm
from django.contrib import messages


def signUp(request):
    if request.method == 'POST':
        signupForm = SignUpForm(request.POST)
        if signupForm.is_valid:
            user = signupForm.save()
            login(request, user)
            return redirect('/')
    else:
        signupForm = SignUpForm()
    return render(request, 'core/base.html', {'signform': signupForm})

def login(request):
    msg = 'Error'
    if request.method == 'POST':
        print('Post')
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            print('valid')
            username = loginForm.cleaned_data.get('username')
            password = loginForm.cleaned_data.get('password')
            print(username, password)

            user = authenticate(request, username=username, password=password)
            print(user.username)
            if user is not None:
                auth_login(request, user)
                return redirect('core:index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            print('Invalid')
            print('Form errors:', loginForm.errors)
            messages.error(request, 'Invalid form submission.')
            return render(request, 'core/index.html', {'msg': msg})
    else:        
        return render(request, 'core/index.html', {'msg':msg})