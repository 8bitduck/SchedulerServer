from bottle import Bottle, route, run, template, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

import requests
import json
import dateutil.parser

JOBS_DATABASE = "postgresql://ubuntu:ubuntu@localhost:5432/SMSSchedulerServer_dev"
# JOBS_DATABASE =
# "postgresql://vagrant:vagrant@localhost:5432/SMSSchedulerServer_dev"
DB_TABLE = "apscheduler_jobs"

SECRET_KEY = "h*|.yUKf37#JBhPCvNI7NAlWLa@:Fqz-GUHK%4H==mU B0+vyWyo*#h{Rgj6nSsb"

# SMSScheduler
# PARSE_APP_ID = "3TYYJK9VqOPj13cYevwxBLtFBOokremx2gM4OBc3"
# PARSE_REST_API_KEY = "LC9PBUbZJLVBFgTiaEIA2mcVrNK7YeDbui3p7Pwr"

# Scheduler
PARSE_APP_ID = "KGhjsUpfVVUfhTFgNG99IhuolVKEBGG51WpfybQJ"
PARSE_REST_API_KEY = "v85f76lacMfbYcRdzHYrSIQcaOkzc605XE0YgDU4"

PARSE_API = "https://api.parse.com/1/functions/"

app = Bottle()

# Calls a Parse Cloud Function
# endpoint - what function do you want to call in Parse Cloud?
# payload - dictionary of what parameters you want to pass to the cloud


def trigger_parse_cloud_function(endpoint, payload):
    headers = {
        'X-Parse-Application-Id': PARSE_APP_ID,
        'X-Parse-REST-API-Key': PARSE_REST_API_KEY,
        'Content-Type': 'application/json'
    }

    url = PARSE_API + endpoint
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print("Parse Response: " + r.text)
    return r

# Called automatically by the scheduler when it is ready to
# send a message to the Parse Cloud.


def trigger_schedule(**kwargs):
    print('Time to Send Schedule! - ' + kwargs['schedule_id'])
    payload = {
        'schedule_id': kwargs['schedule_id']
    }
    trigger_parse_cloud_function('triggerWebhook', payload)

# The endpoint on the server to call with a POST only.
# Must supply the SECRET_KEY to the JSON body to interact
# with the scheduler, otherwise it will fail.
# @Params:
# SECRET_KEY - Your authorization code
# start_timestamp - When do you want to schedule an event?
# message_id - The Parse Messages object ID to identify what
# this schedule correlates to.
#
# @Return - Returns a 'response' string - (error, success)
# If it is successful it will return the job_id of the job.


@app.route('/parseschedule', method='POST')
def parse_create_schedule():
    print("Create Schedule: " + request.json.get('start_timestamp'))
    response = dict()

    # Validate the request
    secret_key = request.json.get('SECRET_KEY')
    if secret_key is None:
        response["response"] = "error"
        response["error"] = "No SECRET_KEY supplied."
        print("Not Scheduling! - " + response["error"])
        return response

    if secret_key != SECRET_KEY:
        response["response"] = "error"
        response["error"] = "Invalid Key"
        print("Not Scheduling! - " + response["error"])
        return response

    schedule_id = request.json.get('schedule_id')
    if schedule_id is None:
        response["response"] = "error"
        response["error"] = "No schedule_id supplied."
        print("Not Scheduling! - " + response["error"])
        return response

    start_timestamp = request.json.get('start_timestamp')
    if start_timestamp is None:
        response["response"] = "error"
        response["error"] = "No start_timestamp supplied."
        print("Not Scheduling! - " + response["error"])
        return response

    # @TODO - validate the start_time and make sure it is after
    # the current time!

    # Request Validated - Create the schedule
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(SQLAlchemyJobStore(url=JOBS_DATABASE,
                                              tablename=DB_TABLE),
                           'default')

    payload = {
        'schedule_id': schedule_id
    }

    job = scheduler.add_job(trigger_schedule,
                            'date',
                            run_date=dateutil.parser.parse(start_timestamp),
                            kwargs=payload)
    scheduler.start()

    response["response"] = "success"
    response["job_id"] = job.id
    print("Job Scheduled - " + job.id)
    return response

# The endpoint that users can call to schedule an event for a trigger.
# This will validate the request and send it to parse for user validation


@app.route('/schedule', method='POST')
def create_schedule():
    print("Validating Account...")
    response = dict()

    # Validate the request

    # Send to Parse to validate
    payload = {
        'API_KEY': request.json.get('API_KEY'),
        'start_timestamp': request.json.get('start_timestamp'),
        'end_timestamp': request.json.get('end_timestamp'),
        'webhook': request.json.get('webhook'),
        'blob': request.json.get('blob')
    }
    r = trigger_parse_cloud_function('validateSchedule', payload)
    if 'error' not in r.json():
        response["response"] = "success"
    else:
        response["response"] = "error"

    print("Response from Parse: " + r.text)
    return response

# A fake Test Webhook that gets called to verify that the scheduler
# works


@app.route('/testWebhook', method='POST')
def test_webhook():
    print("/testWebhook")
    print("Blob Data - " + request.json)
    response = dict()
    response["response"] = "success"
    response["blob"] = request.json
    return response

run(app, server='gunicorn', host='0.0.0.0', port=8080)
# run(app, host='0.0.0.0', port=5000, reloader=True)
