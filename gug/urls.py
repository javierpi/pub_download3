from django.conf.urls import url, include
from .views import google_services, periods, google_services_detail,\
    periods_detail, stat_index_view, index, dspace_detail, api_publication_detail, \
    api_periods_list, api_periods_detail,api_stat
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
app_name = 'gug'



urlpatterns = [
    url(r'^$', index.as_view(), name='index'),
    url(r'^gs/$', google_services.as_view(), name='google_services'),
    url(r'^gs/(?P<pk>\d+)$', google_services_detail.as_view(), name='google_services_detail'),

    url(r'^periods/$', periods.as_view(), name='periods'),
    url(r'^periods/(?P<pk>\d+)$', periods_detail.as_view(), name='periods_detail'),

    url(r'^stat/$', stat_index_view, name='stat_index_paginated'),
    url(r'^dspace/$', dspace_detail, name='dspace_detail'),

    url(r'^api/publication/(?P<pk>[0-9]+)$', api_publication_detail, name='publication-detail'),
    url(r'^api/periods/$', api_periods_list, name='api_periods_list'),
    url(r'^api/periods/(?P<pk>[0-9]+)/$', api_periods_detail, name='api_periods_detail'),
    url(r'^api/stat/$', api_stat),
    
]
urlpatterns = format_suffix_patterns(urlpatterns)