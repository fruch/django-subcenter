from django.conf.urls.defaults import *
from subtitles.models import Subtitle
from transmeta import *
from tagging.views import tagged_object_list

info_dict = {
    'queryset': Subtitle.objects.all(),
}

urlpatterns = patterns('subtitles.views',
    url(r'^add/$', 'add', name='subtitle_add'  ),
)