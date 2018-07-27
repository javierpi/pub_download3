# from jet.dashboard.dashboard_modules import google_analytics_views
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.conf import settings


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
#    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    url(r'^', include('gug.urls')),
]
