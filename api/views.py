from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from twilio.rest import TwilioRestClient

import os

from oauth2_provider.ext.rest_framework import OAuth2Authentication
from SMSSchedulerServer.utils import OAuthTokenIsValid, OAuthTokenHasResourceOwner

# Create your views here.

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
