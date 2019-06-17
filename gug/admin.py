from __future__ import unicode_literals
from django.contrib import admin
from .models import Period, Google_service, Publication, Stats, Dspace, Service_type, Service_group,\
					WorkArea, Extension
from jet.filters import RelatedFieldAjaxListFilter



class Google_service_Admin(admin.ModelAdmin):
    list_display = ('name', 'client_secret_path', 'service', 'group', 'version', 'view_id', 'last_update', 'active')
    list_filter = ('service', 'active') 


class Publication_Admin(admin.ModelAdmin):
    list_display = ('id_dspace', 'tfile', 'id_extension')


class Period_Admin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'active', 'last_update')


class Dspace_Admin(admin.ModelAdmin):
    list_display = ('id_dspace', 'title', 'wacount')
    search_fields = ['title']
    list_filter = ('workarea',)


class Stats_Admin(admin.ModelAdmin):
    list_display = ('google_service', 'period', 'id_dspace', 'publication', 'cuantity')
    list_filter = ('google_service', ('period', RelatedFieldAjaxListFilter), )

class Service_type_Admin(admin.ModelAdmin):
    list_display = ('service', 'max_month_before')
    list_filter = ('service',) 

class WorkArea_Admin(admin.ModelAdmin):
    list_display = ('name',)

class Service_group_admin(admin.ModelAdmin):
    list_display = ('name','order')

class Extension_admin(admin.ModelAdmin):
    list_display = ('name','extension_chars', 'publicationcount')


admin.site.register(Period, Period_Admin)
admin.site.register(Google_service, Google_service_Admin)
admin.site.register(Publication, Publication_Admin)
admin.site.register(Stats, Stats_Admin)
admin.site.register(Dspace, Dspace_Admin)
admin.site.register(Service_type, Service_type_Admin)
admin.site.register(Service_group, Service_group_admin)
admin.site.register(WorkArea, WorkArea_Admin)
admin.site.register(Extension,Extension_admin)

