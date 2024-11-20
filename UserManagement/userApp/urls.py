from django.urls import path
from . import views

urlpatterns = [
   
    path('',views.login,name='login'),
    path('signup/',views.registration,name='signup'),
    path('homepage/',views.homepage,name='homepage'),
    path('userlogout/',views.logout,name='logout'),
    

    

]
