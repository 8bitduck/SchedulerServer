from bottle import Bottle, route, run, template, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

import requests
import json
import dateutil.parser

JOBS_DATABASE = "postgresql://ubuntu:ubuntu@localhost:5432/SMSSchedulerServer_dev"
# JOBS_DATABASE = "postgresql://vagrant:vagrant@localhost:5432/SMSSchedulerServer_dev"
DB_TABLE = "apscheduler_jobs"

SECRET_KEY = "h*|.yUKf37#JBhPCvNI7NAlWLa@:Fqz-GUHK%4H==mU B0+vyWyo*#h{Rgj6nSsb"

PARSE_APP_ID = "3TYYJK9VqOPj13cYevwxBLtFBOokremx2gM4OBc3"
PARSE_REST_API_KEY = "LC9PBUbZJLVBFgTiaEIA2mcVrNK7YeDbui3p7Pwr"
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

# Called automatically by the scheduler when it is ready to
# send a message to the Parse Cloud.


def trigger_message(**kwargs):
    print('Time to Send Message! - ' + kwargs['message_id'])
    payload = {
        'message_id': kwargs['message_id']
    }
    trigger_parse_cloud_function('sendSms', payload)

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


@app.route('/message', method='POST')
def create_message():
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

    message_id = request.json.get('message_id')
    if message_id is None:
        response["response"] = "error"
        response["error"] = "No message_id supplied."
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
        'message_id': message_id
    }

    job = scheduler.add_job(trigger_message,
                            'date',
                            run_date=dateutil.parser.parse(start_timestamp),
                            kwargs=payload)
    scheduler.start()

    response["response"] = "success"
    response["job_id"] = job.id
    print("Job Scheduled - " + job.id)
    return response

run(app, server='gunicorn', host='0.0.0.0', port=8080)
# run(app, host='0.0.0.0', port=5000, reloader=True)
