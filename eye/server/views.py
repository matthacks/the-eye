from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Application, Event, Session
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task, result
from datetime import datetime
import dateutil.parser
import json

def notify_error(task):
    pass

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
    # TODO - add payload validators here
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

def event(request):
    qset = Event.objects.all()
    serialized_qset = serializers.serialize('json', qset)
    return HttpResponse(serialized_qset, content_type='application/json')

def session(request):
    qset = Session.objects.all()
    serialized_qset = serializers.serialize('json', qset)
    return HttpResponse(serialized_qset, content_type='application/json')

@csrf_exempt
def upload(request):
    body = json.loads(request.body.decode('utf-8'))
    session_id = body.get('session_id')
    session = Session.objects.filter(identifier=session_id).first()
    if not session:
        session = Session(identifier=session_id)
        session.save()
    async_task(save_event, body, session, datetime.now())
    return HttpResponse("Received!")