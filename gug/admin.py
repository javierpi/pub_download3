from django.contrib import admin
from .models import Domain, Period, Google_service, Publication, Stats, Dspace


class Publication_Admin(admin.ModelAdmin):
    list_display = ('id_dspace', 'tfile')

class Period_Admin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'active')
     
class Dspace_Admin(admin.ModelAdmin):
    list_display = ('id_dspace', 'title')

class Domain_Admin(admin.ModelAdmin):
    list_display = ('ref', 'name')

class Stats_Admin(admin.ModelAdmin):
	list_display = ('google_service', 'period', 'id_dspace' ,'publication', 'cuantity')

admin.site.register(Domain, Domain_Admin)
admin.site.register(Period, Period_Admin)
admin.site.register(Google_service)
admin.site.register(Publication, Publication_Admin)
admin.site.register(Stats, Stats_Admin)
admin.site.register(Dspace, Dspace_Admin)

