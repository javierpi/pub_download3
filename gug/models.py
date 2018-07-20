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


class Domain(models.Model):

    ref = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique reference ID for this domain")
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Short descriptive name")

    def __str__(self):
        return self.name or self.ref

    def natural_key(self):
        return [self.ref]


class Metric(models.Model):
    #    objects = MetricManager()

    domain = models.ForeignKey(Domain, on_delete=models.PROTECT)
    ref = models.CharField(
        max_length=100,
        help_text="Unique reference ID for this metric within the domain")
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Short descriptive name")
    description = models.TextField(
        blank=True,
        help_text="Description")

    class Meta:
        unique_together = ('domain', 'ref')

    def __str__(self):
        return self.name or self.ref

    def natural_key(self):
        return [self.source, self.ref]


class AbstractStatistic(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    value = models.BigIntegerField(
        # To support storing that no data is available, use: NULL
        null=True)
    period = models.IntegerField(choices=PERIOD_CHOICES)

    class Meta:
        abstract = True


class Period(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField('active', default=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        #return str(self.start_date) + ' - ' + str(self.end_date)
        return str(self.end_date.year) + ' - ' +str(calendar.month_name[self.end_date.month]) 


class Service_type(models.Model):
    service = models.CharField(max_length=20, default='')

    def __str__(self):
        return str(self.service)


class Google_service(models.Model):
    name = models.CharField(max_length=200)
    scope = models.CharField(max_length=200)
    discovery = models.CharField(max_length=200, blank=True, null=True)
    secret_json = models.TextField(default='{}', blank=True, null=True, validators=[validate_json])
    client_secret_path = models.CharField(max_length=100, default='')
    service = models.ForeignKey(Service_type, on_delete=models.CASCADE, null=True)
    version = models.CharField(max_length=2, default='')
    view_id = models.CharField(max_length=30, default='', help_text="In Google Analytics is View Id, in Google Webmaster is protocol+domain")
    active = models.BooleanField('active', default=True)
    report = models.TextField(default='{}', validators=[validate_json], help_text="Transformed variables are view_id, start_date and end_date.")

    def __str__(self):
        return str(self.name)

class Dspace(models.Model):
    id_dspace = models.PositiveIntegerField(default=0, help_text="ID Dspace", unique=True)
    title = models.CharField(max_length=600,default='')

    def __str__(self):
        return str(self.id_dspace) + ' ' + self.title

class Publication(models.Model):
    id_dspace = models.ForeignKey(Dspace, on_delete=models.CASCADE, null=True)
    tfile = models.CharField(max_length=200)

    class Meta:
        ordering = ["id_dspace", "tfile"]
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
        ordering = ["google_service", "publication", "period"]
        unique_together = ("google_service", "period", "id_dspace", "publication")

    def period_desc(self):
        return str(self.period.start_date)

    def __str__(self):
        return str(self.google_service)
