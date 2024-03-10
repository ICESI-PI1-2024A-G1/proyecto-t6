from django.urls import path
from . import views
    
urlpatterns = [
    path('academicUsersLogin/', views.academicUsersLogin, name= 'academicUsersLogin'),
    path('index/', views.index, name='index'),
    path('logout/', views.signout, name= 'logout')
]