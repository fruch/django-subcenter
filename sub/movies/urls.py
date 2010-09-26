from django.conf.urls.defaults import *
from movies.models import Movie
from transmeta import *
from tagging.views import tagged_object_list

info_dict = {
    'queryset': Movie.objects.all().order_by("publish_year"),
}

urlpatterns = patterns('movies.views',
    url(r'^(?P<slug>[-\w]+)/edit/$', 'edit', name='movie_edit'),
    url(r'^(?P<slug>[-\w]+)/delete/$', 'delete', name='movie_delete'),
    url(r'^add/$', 'add', name='movie_add'  ),
    url(r'^imdb_get_info/(?P<format>\w+)/(?P<movie_id>\w+)/$','imdb_get_info', name ='movie_imdb_get_info'),
    url(r'^imdb_search_by_title/(?P<format>\w+)/(?P<title>.*[^/])/$','imdb_search_by_title', name ='movie_imdb_search_by_title'),
)

urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', dict(info_dict, paginate_by=10), name='movie_list'),
    url(r'^(?P<slug>[-\w]+)$', 'object_detail', dict(info_dict, slug_field='slug' ), name='movie_item' ),
    
)

urlpatterns += patterns('',
    url(r'^tag/(?P<tag>[^/]+)/$', tagged_object_list, 
                dict(queryset_or_model=Movie, paginate_by=10, allow_empty=True,
                template_object_name='object'), name='movie_list_by_tag' ),
    
)

