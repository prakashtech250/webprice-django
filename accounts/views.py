from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.contrib import messages

# Create your views here.

def signin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Login successful.")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid username or password.")
        else:
            form = LoginForm()
            if request.user.is_authenticated:
                logout(request)
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('dashboard')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                print('Isss valid')
                user = form.save()
                user.refresh_from_db()
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect('dashboard')
            else:
                print('Not success')
            
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    else:
        return redirect('dashboard')

def forgot_password(request):
    if not request.user.is_authenticated:
        return render(request, 'forgot-password.html')
    else:
        return redirect('dashboard')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('home')
