from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Application, Event, Session
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task, result
from datetime import datetime
import dateutil.parser
import json

def save_event(body, session, scheduled):
    category = body.get('category')
    name = body.get('name')
    data = body.get('data')
    timestamp = dateutil.parser.parse(body.get('timestamp'))
    valid = True
    invalid_reason = ''
    if timestamp >= scheduled:
        valid = False
        invalid_reason = 'Timestamp ({}) is from a future date ({})'.format(timestamp, scheduled)
    # TODO - add a payload validator here
    # TODO - if invalid we could kick off a notification task
    event = Event(
        timestamp=timestamp,
        application=None,
        category=category,
        name=name, 
        payload=data,     
        valid=valid,  
        invalid_reason=invalid_reason,
        session=session
    )
    event.save()

def application(request):
    qset = Application.objects.all()
    serialized_qset = serializers.serialize('json', qset)
    return HttpResponse(serialized_qset, content_type='application/json')

def event(request, session_id=None):
    qset = Event.objects.all()
    if session_id:
        qset = qset.filter(session__identifier=session_id)
    serialized_qset = serializers.serialize('json', qset)
    return HttpResponse(serialized_qset, content_type='application/json')

def session(request, session_id=None):
    qset = Session.objects.all()
    if session_id:
        qset = qset.filter(identifier=session_id)
    serialized_qset = serializers.serialize('json', qset)
    return HttpResponse(serialized_qset, content_type='application/json')

@csrf_exempt # TODO - this decorator was added to be able to connect and quickly run POST requests without reconfiguring project
def upload(request):
    body = json.loads(request.body.decode('utf-8'))
    # TODO - add a check to ensure that the application sending this event is trusted before proceeding
    session_id = body.get('session_id')
    session = Session.objects.filter(identifier=session_id).first()
    if not session:
        session = Session(identifier=session_id)
        session.save()
    async_task(save_event, body, session, datetime.now())
    return HttpResponse("Received!")