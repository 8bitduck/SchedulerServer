# Scheduling Server

## Overview

Bottle App

The scheduling server allows a user to schedule any event and have a webhook get triggered when the time has occured. This server is accomplied by a parse service that powers the rest of the application.

This server's only purpose is to schedule triggers and send the identifier of the schedule (stored in Parse) back to the Parse servers. Parse handles the user authentication and storage of the data. This server has a SECRET_KEY that is stored only in the Parse Server and this Server to validate who the requests are coming from. If Parse sends the right SECRET_KEY, then the request goes through and schedules the event.


## Setup

Light up Vagrant:
  vagrant up

Log into Vagrant:
  vagrant ssh

Install Requirements:
  pip install -r requirements.txt

Run Server:
  python server.py

ENDPOINTS
------------------

### /schedule

##### POST:
Schedules a new event with the scheduling server.

Payload:


