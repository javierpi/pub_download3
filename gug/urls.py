from django.conf.urls import url
from .views import get_GA, get_GCS, google_services, periods, google_services_detail

urlpatterns = [
    url(r'^GA/$', get_GA, name='get_GA'),
    url(r'^GCS/$', get_GCS, name='get_GCS'),
    url(r'^gs/$', google_services.as_view(), name='google_services'),
    url(r'^gs/(?P<pk>\d+)$', google_services_detail.as_view(), name='google_services_detail'),
    url(r'^periods/$', periods.as_view(), name='periods'),

]
