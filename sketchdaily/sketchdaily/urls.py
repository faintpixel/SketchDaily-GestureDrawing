from django.conf.urls import patterns, include, url
from django.contrib import admin
from sketchdaily import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sketchdaily.views.index'),
    url(r'^imageViewer', 'sketchdaily.views.imageViewer'),
    url(r'^startSession', 'sketchdaily.views.startSession'),
    url(r'^help', 'sketchdaily.views.help'),

    # url(r'^sketchdaily/', include('sketchdaily.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
