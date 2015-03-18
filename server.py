from bottle import Bottle, route, run, template, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

import requests
import json
from pytz import utc
import dateutil.parser

JOBS_DATABASE = "postgresql://ubuntu:ubuntu@localhost:5432/SMSSchedulerServer_dev"
# JOBS_DATABASE = "postgresql://vagrant:vagrant@localhost:5432/SMSSchedulerServer_dev"

SECRET_KEY = "h*|.yUKf37#JBhPCvNI7NAlWLa@:Fqz-GUHK%4H==mU B0+vyWyo*#h{Rgj6nSsb"

PARSE_APP_ID = "3TYYJK9VqOPj13cYevwxBLtFBOokremx2gM4OBc3"
PARSE_REST_API_KEY = "LC9PBUbZJLVBFgTiaEIA2mcVrNK7YeDbui3p7Pwr"
PARSE_API = "https://api.parse.com/1/functions/"

app = Bottle()


def trigger_parse_cloud_function(endpoint, payload):
    headers = {
        'X-Parse-Application-Id': PARSE_APP_ID,
        'X-Parse-REST-API-Key': PARSE_REST_API_KEY,
        'Content-Type': 'application/json'
    }

    url = PARSE_API + endpoint
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.text)


def trigger_message(**kwargs):
    print('trigger_message')
    payload = {
        'message_id': kwargs['message_id']
    }
    trigger_parse_cloud_function('sendSms', payload)

# Schedule the message on the server with the message_id that is on Parse


@app.route('/message', method='POST')
def create_message():
    print('/message')
    print(request.json.get('message_id'))
    print(request.json.get('timestamp'))

    secret_key = request.json.get('SECRET_KEY')
    response = dict()

    if secret_key != SECRET_KEY:
        response["response"] = "error"
        response["error"] = "Invalid Key"
    else:
        # Need a timestamp of when to schedule
        # Need a cloud function to call
        # Need an ID to pass back to Parse
        # Store in a database table the ID
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(SQLAlchemyJobStore(url=JOBS_DATABASE,
                                                  tablename='apscheduler_jobs'),
                               'default')

        payload = {
            'message_id': request.json.get('message_id')
        }

        job = scheduler.add_job(trigger_message,
                                'date',
                                run_date=dateutil.parser.parse(
                                    request.json.get('timestamp')),
                                kwargs=payload)
        scheduler.start()

        response["response"] = "success"
        response["job_id"] = job.id
    return response

run(app, server='gunicorn', host='0.0.0.0', port=8080)
# run(app, host='0.0.0.0', port=5000, reloader=True)
