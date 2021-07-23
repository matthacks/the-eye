from django.db import models

# Applications should be recognized as "trusted clients" to "The Eye"
# Applications can send events for the same session
# The Application sending events is responsible for generating the Session identifier
class Application(models.Model):
    created    = models.DateTimeField(auto_now_add=True, editable=False)
    modified   = models.DateTimeField(auto_now=True)
    name       = models.CharField(max_length=255)
    trusted    = models.BooleanField()

# An Event is associated to a Session
class Session(models.Model):
    created    = models.DateTimeField(auto_now_add=True, editable=False)
    modified   = models.DateTimeField(auto_now=True)
    identifier = models.CharField(db_index=True, unique=True, max_length=255)

# An Event has a category, a name and a payload of data (the payload can change according to which event an Application is sending)
# Different types of Events (identified by category + name) can have different validations for their payloads
# Events in a Session should be sequential and ordered by the time they occurred
class Event(models.Model):
    created        = models.DateTimeField(auto_now_add=True, editable=False)
    timestamp      = models.DateTimeField(db_index=True)
    application    = models.ForeignKey(Application, related_name="events", null=True, blank=True, default=None, on_delete=models.SET_NULL)
    session        = models.ForeignKey(Session, related_name="events", null=True, blank=True, default=None, on_delete=models.SET_NULL)
    category       = models.CharField(db_index=True,max_length=255)
    name           = models.CharField(max_length=255)
    payload        = models.JSONField()
    valid          = models.BooleanField(db_index=True)
    invalid_reason = models.TextField(default=None, blank=True, null=True)
