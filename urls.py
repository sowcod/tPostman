from django.conf.urls.defaults import patterns, include, url
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'tpostman.main.views.toppage'),
	url(r'^logout$', 'tpostman.main.views.logout'),
	url(r'^access_token$', 'tpostman.main.views.access_token'),
	url(r'^auth$', 'tpostman.main.views.auth'),
	url(r'^opentweet$', 'tpostman.main.views.opentweet'),

	url(r'^tweet$', 'tpostman.main.api.tweet'),

	url(r'^resources/(?P<path>.*)$', 'django.views.static.serve', 
		{'document_root': os.path.dirname(__file__) + os.sep + 'resources'}),
    # Examples:
    # url(r'^$', 'tpostman.views.home', name='home'),
    # url(r'^tpostman/', include('tpostman.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
