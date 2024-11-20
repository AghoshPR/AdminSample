from django.urls import path
from . import views

urlpatterns = [
    path('adminhome/', views.adminlogin, name='adminhome'),
    path('admhomepage/', views.adminhome, name='admhomepage'),
    path('admlogout/', views.adminlogout, name='admlogout'),
    path('userdelete/<int:user_id>/', views.adminDelete, name='userdelete'),
    path('edituser/<int:user_id>/', views.editUser, name='edituser')


]
