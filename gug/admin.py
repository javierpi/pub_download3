from __future__ import unicode_literals
from django.contrib import admin
from .models import Period, Google_service, Publication, Stats, Dspace, Service_type, Service_group
from jet.filters import RelatedFieldAjaxListFilter


class Google_service_Admin(admin.ModelAdmin):
    list_display = ('name', 'client_secret_path', 'service', 'group', 'version', 'view_id', 'active')


class Publication_Admin(admin.ModelAdmin):
    list_display = ('id_dspace', 'tfile')


class Period_Admin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'active')


class Dspace_Admin(admin.ModelAdmin):
    list_display = ('id_dspace', 'title')
    search_fields = ['title']


class Stats_Admin(admin.ModelAdmin):
    list_display = ('google_service', 'period', 'id_dspace', 'publication', 'cuantity')
    list_filter = ('google_service', ('period', RelatedFieldAjaxListFilter), )


admin.site.register(Period, Period_Admin)
admin.site.register(Google_service, Google_service_Admin)
admin.site.register(Publication, Publication_Admin)
admin.site.register(Stats, Stats_Admin)
admin.site.register(Dspace, Dspace_Admin)
admin.site.register(Service_type)
admin.site.register(Service_group)
