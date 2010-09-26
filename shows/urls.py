from django.conf.urls.defaults import *
from shows.models import Show
from transmeta import *
from tagging.views import tagged_object_list

info_dict = {
    'queryset': Show.objects.all().order_by("years"),
}

urlpatterns = patterns('shows.views',
    #shows
    url(r'^(?P<slug>[-\w]+)/edit/$', 'edit', name='show_edit'),
    url(r'^(?P<slug>[-\w]+)/delete/$', 'delete', name='show_delete'),
    url(r'^add/$', 'add', name='show_add'  ),
    #seasons 
    url(r'^(?P<slug>[-\w]+)/s(?P<season_num>[-\w]+)/$', 'season_details', name='season_item'),
    #url(r'^(?P<slug>[-\w]+)/s(?P<season_num>[-\w]+)/edit/$', 'season_edit', name='season_edit'),
    #episodes
    url(r'^(?P<slug>[-\w]+)/s(?P<season_num>[-\w]+?)/e(?P<episode_slug>[-\w]+?)/$', 'episode_details', name='episode_item'),
    
   
    #ajax calls
    url(r'^imdb_get_info/(?P<format>\w+)/(?P<show_id>\w+)/$','imdb_get_info', name ='show_imdb_get_info'),
    url(r'^imdb_search_by_title/(?P<format>\w+)/(?P<title>.*[^/])/$','imdb_search_by_title', name ='show_imdb_search_by_title'),
    url(r'^fill_show_episodes/(?P<format>\w+)/(?P<title>.*[^/])/$','fill_show_episodes', name ='fill_show_episodes'),
)

urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', dict(info_dict, paginate_by=10), name='show_list'),
    url(r'^(?P<slug>[-\w]+)$', 'object_detail', dict(info_dict, slug_field='slug' ), name='show_item' ),
    
)

urlpatterns += patterns('',
    url(r'^tag/(?P<tag>[^/]+)/$', tagged_object_list, 
                dict(queryset_or_model=Show, paginate_by=10, allow_empty=True,
                template_object_name='object'), name='movie_list_by_tag' ),
    
)
