from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode   
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage  
from django.http import HttpResponse 

# Create your views here.

def signin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    print('Login successful.')
                    messages.success(request, "Login successful.")
                    return redirect('dashboard')
                else:
                    print('Invalid username or password.')
                    messages.error(request, "Invalid username or password.")
        else:
            print('method is get')
            form = LoginForm()
            # if request.user.is_authenticated:
            #     logout(request)
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('dashboard')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            username = request.POST['username']
            email = request.POST['email']
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']
            if User.objects.filter(username=username).exists():
                print('Username already exists. Please try with different username.')
                messages.error(request, 'Username already exists. Please try with different username.')
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                print('Passowrd already exists')
                messages.error(request, 'Email Already exists. Please try with another email')
                return redirect('signup')
            
            if form.is_valid():
                user = User.objects.create_user(username, email, password=pass1)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Please verify your email to activate your account.'
                msg_context = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
                message = render_to_string('activation.html', msg_context)
                print(msg_context)
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')  

                print('Registration successful.')
                messages.success(request, "Registration successful.")
                return redirect('login')
            else:
                print('Not success')
            
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    else:
        return redirect('dashboard')
    
def activate(request, uidb64, token):
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  


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
