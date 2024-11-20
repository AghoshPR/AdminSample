from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as userlogin,logout as userlogout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


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
            error_message='invalid user'

            
    return render(request,'loginpage.html',{'error_message':error_message})
    

def registration(request):

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
        newuser=User(username=reguser,email=regemail,password=regpass)
        newuser.set_password(regpass)
        newuser.save()

        messages.success(request,'Registrtion Successful')
        return redirect('login')


    return render(request,'register.html')

@never_cache
@login_required(login_url='login')

def homepage(request):

    
    
    return render(request,'userhome.html')

def logout(request):
    userlogout(request)
    return redirect('login')