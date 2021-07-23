from django.test import TestCase, Client
from .models import Application, Event, Session
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

class Event(TestCase):
    def test_event_queries(self):
        pass

class Application(TestCase):
    def test_application_queries(self):
        pass

class Session(TestCase):
    def test_session_queries(self):
        pass
