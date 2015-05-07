from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from sketchdaily import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += i18n_patterns('',
url(r'^$', 'sketchdaily.views.index'),
    url(r'^imageViewer', 'sketchdaily.views.imageViewer'),
    url(r'^startSession', 'sketchdaily.views.startSession'),
    url(r'^help', 'sketchdaily.views.help'),
    url(r'^history', 'sketchdaily.views.history'),
    url(r'^json/getReferenceCount/$', 'sketchdaily.views.getReferenceCountJSON'),
)