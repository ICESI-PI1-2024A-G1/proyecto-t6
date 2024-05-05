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
    path('index/', cortex.as_view(), name='index'),
    path('logout/', auth.signout, name='logout'),
    path('create-event-request/', eventRequest.createEventRequest,
         name='create-event-request'),
    path('event-request-record/', eventRequest.eventRequestRecord,
         name='event-request-record'),
    path('event-requests/', eventRequest.eventRequestList,
         name='event-request-list'),
    path('event-list/', event.eventList, name='event-list'),
    path('save-tasks/<int:evento_id>/', event.saveTasks, name='save_tasks'),
    path('event-registry/', event.eventRegistry, name='event-registry'),
    path('finish-event/<int:evento_id>/',
         event.finishEvent, name='finish_event'),
    path('guardar-evento/', event.guardar_evento, name='guardar_evento'),
    path('event-list-apoyo/', event.eventListApoyo, name='event-list-apoyo'),
    path('finish-event-apoyo', event.finishEventApoyo, name='finish-event-apoyo'),
    path('ceremony-plan', event.ceremonyPlan, name='ceremony-plan'),
    path('reset-ceremony/',
         event.reset_ceremony, name='reset_ceremony'),
    path('finish-activity/<int:activity_id>/',
         event.finish_activity, name='finish_activity'),
]
