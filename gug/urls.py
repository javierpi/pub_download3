from django.conf.urls import url
from .views import google_services, periods, google_services_detail,\
			 periods_detail, stat_index_view , index

app_name = 'gug'
urlpatterns = [
    url(r'^$', index.as_view(), name='index'),
    #url(r'^$', periods.as_view(), name='periods'),
    url(r'^gs/$', google_services.as_view(), name='google_services'),
    url(r'^gs/(?P<pk>\d+)$', google_services_detail.as_view(), name='google_services_detail'),
    url(r'^periods/$', periods.as_view(), name='periods'),
    url(r'^periods/(?P<pk>\d+)$', periods_detail.as_view(), name='periods_detail'),
    url(r'^stat/$', stat_index_view, name='stat_index_paginated')
]


