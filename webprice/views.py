from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('account_login')
    # return render(request, 'index.html')
