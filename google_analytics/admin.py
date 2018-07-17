from django.contrib import admin
from .models import Domain, Period


class Domain_Admin(admin.ModelAdmin):
    list_display = ('ref', 'name')


admin.site.register(Domain, Domain_Admin)
admin.site.register(Period)