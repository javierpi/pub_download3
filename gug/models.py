from datetime import date
import json

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


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

    def __str__(self):
        return str(self.start_date)

class Google_service(models.Model):
    name = models.CharField(max_length=200)
    scope = models.CharField(max_length=200)
    discovery = models.CharField(max_length=200)
    secret_json = models.TextField(default='{}', blank=True, null=True, validators=[validate_json])

    def __str__(self):
        return str(self.name)