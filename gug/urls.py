from django.conf.urls import url, include
from .views import google_services, periods, google_services_detail,\
    periods_detail, stat_index_view, index, dspace_detail, periodos_list, periodos_detail
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'gug'
urlpatterns = [
    url(r'^$', index.as_view(), name='index'),
    url(r'^gs/$', google_services.as_view(), name='google_services'),
    url(r'^gs/(?P<pk>\d+)$', google_services_detail.as_view(), name='google_services_detail'),
    url(r'^periods/$', periods.as_view(), name='periods'),
    url(r'^periods/(?P<pk>\d+)$', periods_detail.as_view(), name='periods_detail'),
    url(r'^api/periods/$', periodos_list, name='periodos_list'),
    url(r'^api/periods/(?P<pk>[0-9]+)/$', periodos_detail, name='periodos_detail'),
    
    url(r'^stat/$', stat_index_view, name='stat_index_paginated'),
    url(r'^dspace/$', dspace_detail, name='dspace_detail')
]
urlpatterns = format_suffix_patterns(urlpatterns)