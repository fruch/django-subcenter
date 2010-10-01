from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from userprofile.views import get_profiles
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sub/', include('sub.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
(r'^accounts/', include('userprofile.urls')),
    (r'^$', direct_to_template, {'extra_context': { 'profiles': get_profiles }, 'template': 'front.html'}),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^movies/', include('movies.urls')),
    (r'^actors/', include('persons.urls')),
    (r'^shows/', include('shows.urls')),
    (r'^search/', include('search.urls')),
    (r'^utils/', include('utils.urls')),
    (r'^news/', include('pressroom.urls')),
    (r'^subtitles/', include('subtitles.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),

)
# Serves media content. WARNING!! Only for development uses.
# On production use lighthttpd for media content.
if settings.SERV_STATIC is not None:

    # Delete the first trailing slash, if any.
    if settings.MEDIA_URL.startswith('/'):
        media_url = settings.MEDIA_URL[1:]
    else:
        media_url = settings.MEDIA_URL

    # Add the last trailing slash, if have not.
    if not media_url.endswith('/'):
        media_url = media_url + '/'

    urlpatterns += patterns('',
        (r'^' + media_url + '(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
