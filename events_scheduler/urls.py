from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url('^timeline/$', views.scheduler_timeline, name='timeline')
)
