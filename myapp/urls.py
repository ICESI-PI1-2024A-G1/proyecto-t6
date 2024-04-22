from django.urls import path
from .views import auth
from .views import event
from .views import eventRequest
from .views import cortex

urlpatterns = [
    path('', cortex.home, name ='home'),
    path('academic-members-login/', auth.academicMembersLogin,
         name='academic-members-login'),
    path('ccsa-login/', auth.ccsaLogin, name='ccsa-login'),
    path('index/', cortex.index, name='index'),
    path('logout/', auth.signout, name='logout'),
    path('create-event-request/', eventRequest.createEventRequest,
         name='create-event-request'),
    path('event-request-record/', eventRequest.eventRequestRecord,
         name='event-request-record'),
    path('event-requests/', eventRequest.eventRequestList, name='event-request-list'),
    path('event-list/', event.eventList, name = 'event-list'),
    path('save-tasks/<int:evento_id>/', event.saveTasks, name='save_tasks'),
    path('event-registry/', event.eventRegistry, name = 'event-registry'),
    path('finish-event/<int:evento_id>/', event.finishEvent, name='finish_event'),
]
