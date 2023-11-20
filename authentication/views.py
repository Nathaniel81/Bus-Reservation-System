from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.http import JsonResponse

def signUp(request):
    if request.method == 'POST':
        signupForm = SignUpForm(request.POST)
        if signupForm.is_valid:
            user = signupForm.save()
            auth_login(request, user)
            return JsonResponse({'redirect': '/'})
    else:
        pass
    return render(request, 'core/base.html', {'signform': signupForm})

def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data.get('username')
            password = loginForm.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'redirect': '/'})
            else:
                return JsonResponse({'message': 'Invalid username or password.' })
        else:
            print('Form errors:', loginForm.errors)
            messages.error(request, 'Invalid form submission.')
            return render(request, 'core/index.html', {'msg': 'Invalid form submission.'})
    else:        
        return render(request, 'core/index.html', {'msg':'Not Post'})