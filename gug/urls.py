from django.conf.urls import url, include
from .views import google_services, periods, google_services_detail,\
    periods_detail, stat_index_view, index, dspace_detail, api_publication_detail, \
    api_periods_list, api_periods_detail, get_titles, get_ga, get_workareas, dspace_detail_byfile, \
    dspace_detail_tmp, workareas, groups, extensions

# 

from .apis import get_data, get_report
 

app_name = 'gug'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^stat/$', stat_index_view, name='stat_index_paginated'),

    url(r'^api-auth/', include('rest_framework.urls')),


    url(r'^gs/$', google_services.as_view(), name='google_services'),
    # url(r'^gs/(?P<pk>\d+)$', google_services_detail.as_view(), name='google_services_detail'),
    url(r'^gs/(?P<pk>\d+)$', google_services_detail, name='google_services_detail'),

    url(r'^periods/$', periods.as_view(), name='periods'),
    # url(r'^periods/(?P<pk>\d+)$', periods_detail.as_view(), name='periods_detail'),
    url(r'^periods/(?P<pk>\d+)$', periods_detail, name='periods_detail'),

    url(r'^extensions/$', extensions.as_view(), name='extensions'),

    url(r'^workareas/$', workareas, name='workareas'),
    url(r'^groups/$', groups, name='groups'),

    url(r'^dspace/$', dspace_detail, name='dspace_detail'),
    url(r'^dspace_tmp/$', dspace_detail_tmp, name='dspace_detail_tmp'),
    url(r'^dspace_tmp/(?P<id_dspace>\d+)$', dspace_detail_byfile, name='dspace_detail_byfile'),
    

    url(r'^api/publication/(?P<pk>[0-9]+)$', api_publication_detail, name='publication-detail'),
    url(r'^api/periods/$', api_periods_list, name='api_periods_list'),
    url(r'^api/periods/(?P<pk>[0-9]+)/$', api_periods_detail, name='api_periods_detail'),

    # API to get data
    url(r'^get_data/$', get_data.as_view()),
    url(r'^get_report/$', get_report.as_view() , name='get_report'),
    

    # Commands
    url(r'^get_titles/$', get_titles, name='get_titles'),
    url(r'^get_ga/$', get_ga, name='get_GA'),
    url(r'^get_workareas/$', get_workareas, name='get_workareas')
    
]

