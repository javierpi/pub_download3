from django.conf.urls import url
from .views import get_GA, get_GCS, google_services, periods, google_services_detail,\
			 periods_detail, stat_index_view

urlpatterns = [
    url(r'^GA/$', get_GA, name='get_GA'),
    url(r'^GCS/$', get_GCS, name='get_GCS'),
    url(r'^gs/$', google_services.as_view(), name='google_services'),
    url(r'^gs/(?P<pk>\d+)$', google_services_detail.as_view(), name='google_services_detail'),
    url(r'^periods/$', periods.as_view(), name='periods'),
    url(r'^periods/(?P<pk>\d+)$', periods_detail.as_view(), name='periods_detail'),
    url(r'^stat/(?P<gs>\d+)/(?P<period>\d+)/$', stat_index_view, name='stat_index_paginated')
]


