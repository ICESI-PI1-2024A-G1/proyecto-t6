from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('academic-members-login/', views.academicMembersLogin,
         name='academic-members-login'),
    path('ccsa-login/', views.ccsaLogin, name='ccsa-login'),
    path('index/', views.index, name='index'),
    path('logout/', views.signout, name='logout'),
    path('create-event-request/', views.createEventRequest,
         name='create-event-request'),
    path('event-record/', views.eventRecord,
         name='event-record'),
    path('events/', views.eventsList, name='events-list'),
]
