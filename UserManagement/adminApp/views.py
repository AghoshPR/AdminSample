from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.contrib import messages

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
            messages.success(request,'Ivalid User')
   
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


def adminlogout(request):
    logout(request)
    return redirect('login')


#................adminHomepage ends.................

#................adminDelete.................

def adminDelete(request,user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    messages.success(request,'deleted successfully')
    return redirect(adminhome)


#................adminDelete Ends.................

#................adminEdit...................

def editUser(request,user_id):
    user=get_object_or_404(User,id=user_id)
    
    if request.POST:
        edituser=request.POST['edituser']
        editemail=request.POST['editemail']

        user.username=edituser
        user.email=editemail
        user.save()
        messages.success(request,'user deatils updated succefully')
        return redirect('admhomepage')
          
    return render(request,'useredit.html',{'user':user})
        


#................adminEdit ends...............





    