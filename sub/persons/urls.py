from django.conf.urls.defaults import *
from persons.models import Actor
from transmeta import *
from tagging.views import tagged_object_list

info_dict = {
    'queryset': Actor.objects.all().order_by('name_en'),
}

urlpatterns = patterns('persons.views',
    url(r'^(?P<slug>[-\w]+)/edit/$', 'actor_edit', name='actor_edit'),
    url(r'^(?P<slug>[-\w]+)/delete/$', 'actor_delete', name='actor_delete'),
    url(r'^add/$', 'actor_add', name='actor_add'  ),
    url(r'^imdb_get_info/(?P<format>\w+)/(?P<person_id>\w+)/$','imdb_get_info', name ='per_imdb_get_info'),
    url(r'^imdb_search_by_name/(?P<format>\w+)/(?P<name>.*[^/])/$','imdb_search_by_name', name ='per_imdb_search_by_name'),
    url(r'^edb_translate_name/(?P<format>\w+)/(?P<name>.*[^/])/$','edb_translate_name', name ='edb_translate_name'),

)

urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', dict(info_dict,paginate_by=10) , name='actor_list'),
    url(r'^(?P<slug>[-\w]+)$', 'object_detail', dict(info_dict, slug_field='slug' ), name='actor_item' ),    
)

urlpatterns += patterns('',
    url(r'^tag/(?P<tag>[^/]+)/$', tagged_object_list, 
                dict(queryset_or_model=Actor, paginate_by=10, allow_empty=True,
                template_object_name='object'), name='actor_list_by_tag' ),
    
)

