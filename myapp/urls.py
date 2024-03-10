from django.urls import path
from . import views

urlpatterns = {
    path('academicMembersLogin/', views.academicMembersLogin, name= 'academicMembersLogin'),
    path('index/', views.index, name='index'),
    path('logout/', views.signout, name= 'logout')
}