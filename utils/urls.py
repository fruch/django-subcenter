from django.conf.urls.defaults import *
from djcelery.views import  task_status

urlpatterns = patterns('',
    url('^task-stat/(?P<task_id>[-\w]+)/$', task_status, name='task_status'),
)
