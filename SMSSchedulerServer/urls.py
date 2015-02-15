from django.conf.urls import patterns, url, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

admin.autodiscover()

urlpatterns = patterns('',
   url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^api/', include('api.urls')),
)