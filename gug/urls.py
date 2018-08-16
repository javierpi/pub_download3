from django.conf.urls import url, include
from .views import google_services, periods, google_services_detail,\
    periods_detail, stat_index_view, index, dspace_detail, api_publication_detail, \
    api_periods_list, api_periods_detail, get_titles
from .apis import get_data

# class StatsViewSet(viewsets.ModelViewSet):
#     queryset = Stats.objects.all()
#     serializer_class = StatsSerializer

#     @classmethod
#     def get_extra_actions(cls):
#         return []


# router = routers.DefaultRouter()
# router.register(r'stat2', StatsViewSet, base_name='inoutreports')

app_name = 'gug'

urlpatterns = [
    #url(r'^$', index.as_view(), name='index'),
    url(r'^$', index.as_view(), name='index'),
    url(r'^stat/$', stat_index_view, name='stat_index_paginated'),

    # url(r'^api/', include((router.urls, 'app_name'), namespace='instance_name')),
    url(r'^api-auth/', include('rest_framework.urls')),


    url(r'^gs/$', google_services.as_view(), name='google_services'),
    url(r'^gs/(?P<pk>\d+)$', google_services_detail.as_view(), name='google_services_detail'),

    url(r'^periods/$', periods.as_view(), name='periods'),
    url(r'^periods/(?P<pk>\d+)$', periods_detail.as_view(), name='periods_detail'),

    url(r'^dspace/$', dspace_detail, name='dspace_detail'),

    url(r'^api/publication/(?P<pk>[0-9]+)$', api_publication_detail, name='publication-detail'),
    url(r'^api/periods/$', api_periods_list, name='api_periods_list'),
    url(r'^api/periods/(?P<pk>[0-9]+)/$', api_periods_detail, name='api_periods_detail'),

    # API to get data
    url(r'^get_data/$', get_data.as_view()),
    #    url(r'^api/chart/data/(?P<pk>\d+)/(?P<ctype>[\w]+)/$', ChartData2.as_view()),

    # Commands
    url(r'^get_title/(?P<dspace_id>[0-9]+)$', get_titles, name='get_titles')
]
# urlpatterns = format_suffix_patterns(urlpatterns)
