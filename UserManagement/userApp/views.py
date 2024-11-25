from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as userlogin,logout as userlogout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


@never_cache
def login(request):
    error_message=None
    
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.POST:
        username=request.POST['usr']
        password=request.POST['psd']

        user=authenticate(username=username,password=password)
        if user:
            userlogin(request,user)
            return redirect('homepage')
    
        else:
            error_message='invalid username or password'

            
    return render(request,'loginpage.html',{'error_message':error_message})
    
@never_cache
def registration(request):

    if request.user.is_authenticated:
        return redirect('homepage')


    if request.POST:
        reguser=request.POST['regusr']
        regpass=request.POST['regpass']
        regconpass=request.POST['regconpass']
        regemail=request.POST['regemail']

        if regpass != regconpass:
            messages.error(request,'password donot match')
            return render(request,'register.html')
        

        if User.objects.filter(username=reguser).exists():
            messages.error(request,'Username already exists!')
            return render(request,'register.html')
        
        try:
            validate_email(regemail)
        except ValidationError:
            messages.error(request,'Invalid email format')
            return render(request,'register.html')

        messages.success(request,'Registration Successful')
        newuser=User(username=reguser,email=regemail,password=regpass)
        newuser.set_password(regpass)
        newuser.save()

        
        return redirect('login')


    return render(request,'register.html')

@never_cache
@login_required(login_url='login')

@never_cache
def homepage(request):

    return render(request,'userhome.html')

def logout(request):
    userlogout(request)
    return redirect('login')