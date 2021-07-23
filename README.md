# the-eye

### Project Overview
-----------------------
The Eye see's all. This is a simple application that demontrates building a REST API with Django and kicking off asynchronous tasks using django-q/Redis.

### Installation/Set-Up
-----------------------
Instructions at this time are for a MacOS Environent

Pre-reqs:
- python3.9
- pipenv
- redis

-----------------------
Clone the repository and then via terminal navigate to the main project folder and run 'pipenv install'.

Once the installation is complete, you will need to complete the following:

1. start local redis server with default settings
2. run the following command in a pipenv shell: ./manage.py qcluster
3. run the following command in another pipenv shell: ./manage.py runserver

THE EYE IS NOW READY TO ACCEPT YOUR LOCAL CONNECTIONS!

You can run tests with: ./manage.py test

### Available URLS
-----------------------
POST: '/server/upload'
-----------------------
This URL accepts a POST request where the body contains JSON event data.
A new session will be created based on the session_id if it does not already exist in the system, and then an async task is kicked off where the event will be parsed, validated, and saved.

GET: '/server/event'
-----------------------
This will return all of the events in the system.

GET: '/server/event/<session_id>'
-----------------------
This will return all of the events in the system that are related to the session_id

GET: '/server/session'
-----------------------
This will return all of the sessions in the system.

GET: '/server/session<session_id>'
-----------------------
This will return all of the sessions in the system where the identifier equals the session_id


GET: '/server/application'
-----------------------
This will return all of the applications in the system.

### ASSUMPTIONS/CONCLUSIONS
-----------------------
- all data in the payload is assumed to be accessible and able to be parsed without error (this is only for the shell software's sake. in a production program we would absolutely validate each field)
- string data will not exceed 255 characters
- session ID's are unique
- timestamps are sent in UTC
- the client should be expecting JSON responses when hitting the API
- a future iteration will parse the payload's host and save the application data into the system, so we could then validate that it is trusted before saving event/session info
- a future iterations will support deeper queries of system data using search terms, filters, etc.
- much more cleanup/tweaking of defaults would take place in a production program; this version is quick and dirty