from django.conf.urls import url
from .views import get_GA, get_GCS

urlpatterns = [
    url(r'^GA/$', get_GA, name='get_GA'),
    url(r'^GCS/$', get_GCS, name='get_GCS'),
]
