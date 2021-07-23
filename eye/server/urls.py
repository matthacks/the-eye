from django.urls import path

from . import views

urlpatterns = [
    path('event', views.event, name='event'),
    path('event/<path:session_id>', views.event, name='event'),
    path('application', views.application, name='application'),
    path('session', views.session, name='session'),  
    path('session/<path:session_id>', views.session, name='session'),
    path('upload', views.upload, name='upload'),
]