from django.test import TestCase, Client
from .models import Application, Event, Session
from datetime import datetime
import json

# THIS IS JUST THE BEGINNING; YOU CAN NEVER HAVE ENOUGH TESTS

class Creation(TestCase):
    def test_provided_examples(self):
        """Test Save"""
        c = Client()
        EXAMPLES = [{
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "page interaction",
            "name": "pageview",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
            },
            "timestamp": "2021-01-01 09:15:27.243860"
            },
            {
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "page interaction",
            "name": "cta click",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
                "element": "chat bubble"
            },
            "timestamp": "2021-01-01 09:15:27.243860"
            },
            {
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "form interaction",
            "name": "submit",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
                "form": {
                "first_name": "John",
                "last_name": "Doe"
                }
            },
            "timestamp": "2021-01-01 09:15:27.243860"
        }]
        for ex in EXAMPLES:
            response = c.post('/server/upload', ex, content_type='application/json')
            self.assertEqual(response.status_code, 200)
        response = c.get('/server/session')
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content)
        self.assertEqual(len(resp), 1)
        response = c.get('/server/event')
        self.assertEqual(response.status_code, 200) # TODO - this isn't actually a great test since tasks are still using the dev database...

    # TODO - place holder tests
    def test_stress(self):
        pass
    
    def test_invalid(self):
        pass
    
    def test_future_date(self):
        pass

class Queries(TestCase):
    def setUp(self):
        app = Application.objects.create(name="www.consumeraffairs.com", trusted=True)
        session = Session.objects.create(identifier="1234564789-ABCD")
        Event.objects.create(timestamp=datetime.now(), application=app, session=session, category = 'page interaction', name='pageview',
            payload = { "host": "www.consumeraffairs.com", "path": "/", "element": "chat bubble" }, valid=True, invalid_reason = None
        )
        Event.objects.create(timestamp=datetime.now(), application=app, session=session, category = 'page interaction', name='btn click',
            payload = { "host": "www.consumeraffairs.com", "path": "/", "element": "chat bubble" }, valid=False, invalid_reason = 'Time is from future...'
        )
        session = Session.objects.create(identifier="ABCD-1234564789")
        Event.objects.create(timestamp=datetime.now(), application=app, session=session, category = 'page interaction', name='pageview',
            payload = { "host": "www.consumeraffairs.com", "path": "/", "element": "chat bubble" }, valid=True, invalid_reason = None
        )

    def test_application_queries(self):
        c = Client()
        response = c.get('/server/application')
        resp = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 1)

    def test_event_queries(self):
        c = Client()
        response = c.get('/server/event')
        resp = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 3)

        response = c.get('/server/event/1234564789-ABCD')
        resp = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 2)

        response = c.get('/server/event/ABCD-1234564789')
        resp = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 1)

        response = c.get('/server/event/ABCD')
        resp = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 0)

    def test_session_queries(self):
        c = Client()
        response = c.get('/server/session')
        resp = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 2)

        response = c.get('/server/session/1234564789-ABCD')
        resp = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 1)

        response = c.get('/server/session/ABCD-1234564789')
        resp = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 1)

        response = c.get('/server/session/ABCD')
        resp = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp), 0)
