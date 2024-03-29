from datetime import date
import json
import calendar

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.core.exceptions import ValidationError


class Period(object):
    DAY = 86400  # seconds
    WEEK = DAY * 7
    DAYS_28 = DAY * 28
    MONTH = DAY * 30
    LIFETIME = 0


PERIOD_CHOICES = (
    (Period.DAY, 'Day'),
    (Period.WEEK, 'Week'),
    (Period.DAYS_28, '28 days'),
    (Period.MONTH, 'Month'),
    (Period.LIFETIME, 'Lifetime'))


def validate_json(value):
    try:
        json.loads(value)
    except ValueError:
        raise ValidationError(('Variables must be in json format'), params={},)


class Period(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField('active', default=True)
    last_update = models.DateField(auto_now=True)
    # closed = models.BooleanField('Data on this period is gotten', default=False)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return str(self.end_date.year) + ' - ' + str(calendar.month_name[self.end_date.month])

    @staticmethod
    def autocomplete_search_fields():
        return 'start_date',


class Service_type(models.Model):
    service = models.CharField(max_length=20, default='')
    max_month_before = models.PositiveSmallIntegerField(default=0, help_text="Month service deliver stats")

    class Meta:
        verbose_name_plural = 'Service types'
        verbose_name = 'Service type'

    def __str__(self):
        return str(self.service)

    @staticmethod
    def autocomplete_search_fields():
        return 'service',


class Service_group(models.Model):
    name = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Service groups'
        verbose_name = 'Service group'
        ordering = ["order"]

    def __str__(self):
        return str(self.name)

    @staticmethod
    def autocomplete_search_fields():
        return 'name',


class Google_service(models.Model):
    name = models.CharField(max_length=200)
    scope = models.CharField(max_length=200)
    discovery = models.CharField(max_length=200, blank=True, null=True)
    secret_json = models.TextField(default='{}', blank=True, null=True, validators=[validate_json])
    client_secret_path = models.CharField(max_length=100, default='')
    service = models.ForeignKey(Service_type, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Service_group, default=1, on_delete=models.CASCADE, null=True)
    version = models.CharField(max_length=2, default='')
    view_id = models.CharField(max_length=60, default='', help_text="In Google Analytics is View Id, in Google Webmaster is protocol+domain")
    active = models.BooleanField('active', default=True)
    report = models.TextField(default='{}', validators=[validate_json], help_text="Transformed variables are view_id, start_date and end_date.")
    last_update = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Google Services'
        verbose_name = 'Google Service'

    def __str__(self):
        return str(self.name) 
        # + ' :(Grpid:' + str(group.id)

    @staticmethod
    def autocomplete_search_fields():
        return 'name',


class WorkArea(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]


    def __str__(self):
        return str(self.name)

    @staticmethod
    def autocomplete_search_fields():
        return 'name',


class Dspace(models.Model):
    id_dspace = models.PositiveIntegerField(default=0, help_text="ID Dspace", unique=True)
    title = models.CharField(max_length=600, default='')
    post_title1 = models.CharField(max_length=300, default='')
    post_title2 = models.CharField(max_length=200, default='')
    workarea = models.ManyToManyField(WorkArea, related_name='workareas', blank=True)

    def __str__(self):
        return str(self.id_dspace) + ' ' + self.title.split('|')[0]

    def title_short(self):
        return self.title.split('|')[0]

    def wacount(self):
        return self.workarea.count()


    @staticmethod
    def autocomplete_search_fields():
        return 'title', 'id_dspace'

class Extension(models.Model):
    name = models.CharField(max_length=100, default='')
    extension_chars = models.CharField(max_length=10, default='')

    def __str__(self):
        return str(self.extension_chars)

    def publicationcount(self):
        return Publication.objects.filter(id_extension=self.id).count()
        

class Publication(models.Model):
    id_dspace = models.ForeignKey(Dspace, on_delete=models.CASCADE, null=True)
    tfile = models.CharField(max_length=200)
    id_extension = models.ForeignKey(Extension, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["id_dspace", "tfile", "id_extension"]
        unique_together = ("id_dspace", "tfile")

    def __str__(self):
        return str(self.tfile)


class Stats(models.Model):
    google_service = models.ForeignKey(Google_service, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.PROTECT)
    id_dspace = models.ForeignKey(Dspace, on_delete=models.CASCADE, null=True)
    publication = models.ForeignKey(Publication, on_delete=models.PROTECT)
    cuantity = models.BigIntegerField(null=True)

    class Meta:
        verbose_name_plural = 'STATS'
        verbose_name = 'STATS'
        indexes = [
            models.Index(
                fields=['id_dspace', 'google_service', 'period'],
                name='stats_iddspace_idx',
            ),
        ]
        ordering = ["google_service", "publication", "period"]
        unique_together = ("google_service", "period", "id_dspace", "publication")

    def period_desc(self):
        return str(self.period.start_date)

    def __str__(self):
        return str(self.google_service)
