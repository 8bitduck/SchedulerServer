from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^endpoint/?$', views.ExampleEndpointView.as_view(), name='endpoint_test'),
    url(r'^schedule/?$', views.ScheduleExample.as_view(), name='schedule'),

	url(r'^messages/?$', views.MessagesCollectionView.as_view(), name='message_collection'), 
	url(r'^messages/(?P<id>[a-zA-Z0-9-_]+)/?$', views.MessagesView.as_view(), name='message_resource'), 
	url(r'^lists/?$', views.ListsCollectionView.as_view(), name='lists_collection'),
	url(r'^lists/(?P<id>[a-zA-Z0-9-_]+)/?$', views.ListsView.as_view(), name='list_resource'),
	url(r'^users/?$', views.UserCollectionView.as_view(), name='user_collection'),
	url(r'^users/(?P<id>[a-zA-Z0-9-_]+)/?$', views.UserView.as_view(), name='user_resource'),
	
)