from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url('(?P<pk>\d+)/map/', 'schedule.views.map'),
    url('(?P<pk>\d+)/', 'schedule.views.show')
)
