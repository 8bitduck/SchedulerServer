from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import User

from twilio.rest import TwilioRestClient
from SMSSchedulerServer.validators import is_password_valid

from api.serializers import *
from accounts.serializers import *

import os

from oauth2_provider.ext.rest_framework import OAuth2Authentication
from SMSSchedulerServer.utils import OAuthTokenIsValid, OAuthTokenHasResourceOwner

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

JOBS_DATABASE = "postgresql://localhost:3000/SMSSchedulerServer_dev"

def tick():
    print('Tick!')

# Create your views here.

class ScheduleExample(APIView):
    permission_classes = (OAuthTokenHasResourceOwner,)

    def get(self, request, format=None):

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(SQLAlchemyJobStore(url=JOBS_DATABASE, tablename='apscheduler_jobs'), 'default')
        scheduler.add_job(tick, 'interval', seconds=3)
        scheduler.start()

        ev = {
            "id": 200,
            "test": "ScheduleEndpoint"
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response


class ExampleEndpointView(APIView):
    permission_classes = (OAuthTokenHasResourceOwner,)

    """
    Documentation
    """
    def get(self, request, format=None):

        client = TwilioRestClient(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
        message = client.messages.create(   body="Test Message", 
                                            to="+15129343410",
                                            from_="+15125808070")

        ev = {
            "id": 100,
            "test": "Test Endpoint was successful!",
            "twilio_id": message.sid
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

class MessagesCollectionView(APIView):
    permission_classes = (OAuthTokenHasResourceOwner,)

    def get(self, request, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

    def post(self, request, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

class MessagesView(APIView):
    permission_classes = (OAuthTokenHasResourceOwner,)

    def get(self, request, id, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

    def delete(self, request, id, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

    def put(self, request, id, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

class ListsCollectionView(APIView):
    permission_classes = (OAuthTokenHasResourceOwner,)

    def get(self, request, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

    def post(self, request, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

class ListsView(APIView):
    permission_classes = (OAuthTokenHasResourceOwner,)

    def get(self, request, id, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

    def put(self, request, id, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

    def delete(self, request, id, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

class UserCollectionView(APIView):

    def post(self, request, format=None):

        serializer = UserSerializer(data=request.DATA)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)

        return Response({
                "error": "validation_failed",
                "error_description": "User resource is not valid.",
                "field_errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST) 

class UserView(APIView):
    permission_classes = (OAuthTokenHasResourceOwner,)

    def get(self, request, id, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

    def put(self, request, id, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response

    def delete(self, request, id, format=None):
        ev = {
            "id": 200
        }

        response = Response(data=[ev])

        # Cache Control
        response['Cache-Control'] = "no-transform,private,s-maxage=3600,max-age=3600"
        response['Vary'] = 'Accept-Encoding'
        return response