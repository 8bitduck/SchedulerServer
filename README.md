# SMS Scheduling Server

## Overview

The scheduling server allows a user to schedule an SMS/MMS message to be sent to a phone list of the users choosing. This server is accomplied by a native iOS Application. 


## Setup

Light up Vagrant:
  vagrant up

Log into Vagrant:
  vagrant ssh

Install Requirements:
  pip install -r requirements.txt

Sync Database:
  ./manage syncdb

Run Server:
  ./manage.py runserver [::]:3000

Also, when you create the virtual machine, the host will connect to
localhost:3000,  if for some reason you have this port in use already,
alter the line in Vagrantfile that looks like:

    config.vm.network :forwarded_port, guest: 3000, host: 3000, id: "django"

Edit the "host: 3000" part to reflect the port you wish to use.

Example API Endpoint
--------------------

You will need to login into the /admin site and generate an site API AOuth Application.

Create a new Application in the Django Admin under OAuth2_Provider.

`Client Id:` abc

`User:` 1 (Your defautl vagrant user you created)

`Client Type:` Confidential

`Authorization Grant Type:` Resource owner password-based

`Client Secret:` 123

`Name:` TestApp

Now you can get your users token:

`curl -u abc:123 -X POST http://localhost:3000/oauth/token/ -d 'grant_type=password&username=vagrant&password=vagrant'`

Save the Access Token you receive.  

There is an Endpoint.paw file included that will allow you to test the endpoint. Paste your Access Token into the Bearer token field in the OAuth2Authorization and run the example.  

The CURL Command: 
`curl -X "GET" "http://localhost:3000/api/endpoint/" \
	-H "Authorization: Bearer <ACCESS TOKEN>"`

Testing
-------

[Nose Test Runner](https://nose.readthedocs.org/en/latest/)

[Django Rest Framework testing documentation](http://www.django-rest-framework.org/api-guide/testing)


Model Updates
-------------

After editing your models.py, run:

    ./manage.py schemamigration <app>  --auto
    ./manage.py migrate <app>

REST API ENDPOINTS
------------------

### /api/message/

##### POST:

##### GET:

##### DELETE:

##### PUT:

---

### /api/lists/

##### GET:

---
### /api/list/

##### POST:

##### GET:

##### DELETE:

##### PUT:

---

### /api/profile/

##### PUT:

##### GET:

---

### /api/register/

##### POST:

---

### /api/login/

##### POST:

---

### /api/logout/

##### POST:
