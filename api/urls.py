from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^endpoint/?$', views.ExampleEndpointView.as_view(), name='endpoint_test'),
    url(r'^schedule/?$', views.ScheduleExample.as_view(), name='schedule'),

	url(r'^message/?$', views.Message.as_view(), name='message'), 
	url(r'^lists/?$', views.Lists.as_view(), name='lists'),
	url(r'^list/?$', views.List.as_view(), name='list'),
	url(r'^profile/?$', views.Profile.as_view(), name='profile'),
	url(r'^register/?$', views.Register.as_view(), name='register'), 
	url(r'^login/?$', views.Login.as_view(), name='login'),
	url(r'^logout/?$', views.Logout.as_view(), name='logout'),        
)