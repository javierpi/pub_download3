# from jet.dashboard.dashboard_modules import google_analytics_views
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from gug.serializers import DspaceViewSet, PublicationViewSet, Service_typeViewSet, PeriodViewSet, Google_serviceViewSet, StatsViewSet


# from gug.serializers import DspaceSerializer, PublicationSerializer, Service_typeSerializer, Google_serviceSerializer, PeriodSerializer, DspaceViewSet, PublicationViewSet, Service_typeViewSet, PeriodViewSet, Google_serviceViewSet, StatsSerializer, StatsViewSet
# from gug.models import Google_service, Period, Publication, Stats, Dspace, Service_type


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'period', PeriodViewSet)
router.register(r'google_service', Google_serviceViewSet)
router.register(r'service_type', Service_typeViewSet)
router.register(r'publication', PublicationViewSet)
router.register(r'dspace', DspaceViewSet)
router.register(r'stats', StatsViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    url(r'^', include('gug.urls')),
    url(r'^api-auth/', include('rest_framework.urls'))
]
