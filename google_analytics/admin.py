from django.contrib import admin
from .models import Domain, Period, Google_service


class Domain_Admin(admin.ModelAdmin):
    list_display = ('ref', 'name')


admin.site.register(Domain, Domain_Admin)
admin.site.register(Period)
admin.site.register(Google_service)