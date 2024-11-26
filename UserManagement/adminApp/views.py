from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

#................adminlogin.................
@never_cache
def adminlogin(request):

    if request.user.is_authenticated:
        return redirect('admhomepage')
    
    if request.POST:
        aduser=request.POST['adusr']
        adpass=request.POST['adpass']

        user=authenticate(username=aduser,password=adpass)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('admhomepage')  
        else:
            messages.success(request,'Invalid User')
   
    return render(request,'adminlogin.html')

#................adminlogin ends.................



#................adminHomepage.................

@login_required(login_url='login')
@never_cache
def adminhome(request):
    query=request.GET.get('q','')
    if query:
        users=User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query) ) #filtering the users
    else:
        users=User.objects.all()

    context = {
    'users': users, 
    'query': query  
}
    return render(request,'adminhome.html',context) 

@login_required(login_url='login')
def adminlogout(request):
    logout(request)
    return redirect('login')


#................adminHomepage ends.................

# ...............adminUserCreate....................
@login_required(login_url='login')
def adduser(request):

    if request.POST:
        cuser=request.POST['cuser'].strip()
        cpass=request.POST['cpass'].strip()
        cemail=request.POST['cemail'].strip()

        if not cuser or not cpass or not cemail:
            messages.error(request,'All fields are Required')
            return render(request,'adduser.html')
        
        try:
            validate_email(cemail)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return render(request, 'adduser.html')

        if len(cpass)<6:
            messages.error(request,'Password must contain 6 characters')
            return render(request,'adduser.html')

        if User.objects.filter(username=cuser).exists():
            messages.error(request,'User already Exists.')
        else:
            User.objects.create_user(username=cuser,password=cpass,email=cemail)
            messages.success(request,'User Created Successfully')
            return redirect('admhomepage')


    return render(request,'adduser.html')


# ...............adminUserCreate ends....................


#................adminDelete.................
@login_required(login_url='login')
@never_cache

def adminDelete(request,user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    messages.success(request,'Deleted successfully')
    return redirect(adminhome)


#................adminDelete Ends.................

#................adminEdit...................
@login_required(login_url='login')
@never_cache
def editUser(request,user_id):
    user=get_object_or_404(User,id=user_id)
    
    if request.POST:
        edituser=request.POST['edituser'].strip()
        editemail=request.POST['editemail'].strip()

        if not edituser:
            messages.error(request,'username cannot be Empty!')
            return render(request,'useredit.html',{'user':user})

        if not editemail:
            messages.error(request,'Email cannot be Empty!')
            return render(request,'useredit.html',{'user':user})

        try:
            validate_email(editemail)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return render(request, 'useredit.html',{'user':user})

        user.username=edituser
        user.email=editemail
        user.save()
        messages.success(request,'User deatils updated successfully')
        return redirect('admhomepage')
          
    return render(request,'useredit.html',{'user':user})
        


#................adminEdit ends...............





    