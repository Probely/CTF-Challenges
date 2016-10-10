from django.conf.urls import patterns, include, url

# Serving static files requires "DEBUG=True" anyway...
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('app.views',
    url(r'^$', 'index', name='index'),
    url(r'^login$', 'login'),
    url(r'^logout/$', 'logout'),
    url(r'^error_auth/$', 'error_auth'),
    url(r'^viewmail/(\w+)/$', 'viewmail'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
