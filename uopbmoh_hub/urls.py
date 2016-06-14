import os
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.site.site_header = os.environ.get('UOPBMOH_HUB_TITLE', 'UoPBMoH Admin')


urlpatterns = patterns(
    '',
    url(r'^admin/',  include(admin.site.urls)),
    url(r'^', include('hub.urls')),
)
