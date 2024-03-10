from django.urls import path
from . import views
    
urlpatterns = [
    path('academic_users_login/', views.academicUsersLogin, name= 'academicUsersLogin'),
    path('index/', views.index, name='index'),
    path('logout/', views.signout, name= 'logout'),
    path('create-event-request/', views.create_event_request, name='create_event_request'),
]