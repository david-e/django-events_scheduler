from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^timeline/(?P<view>\w)/$', views.scheduler_timeline, name='timeline'),
    url(r'^dp/$', views.data_processor, name='data_processor'),
)
