from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^endpoint/?$', views.ExampleEndpointView.as_view(), name='endpoint_test'),
)