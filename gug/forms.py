from django import forms
from gug.models import Google_service, Period, Dspace


class DspaceForm(forms.Form):
    gs_choices = Google_service.objects.all().values_list('id', 'name')
    detail = forms.BooleanField(label="Detailed report", required=False)
    period_choices = Period.objects.all().values_list('id', 'start_date')

    period = forms.MultipleChoiceField(choices=period_choices, label="Period")
    # id_dspace_choices = Dspace.objects.all().values_list('id_dspace','id_dspace')

    id_dspace = forms.IntegerField(label="Dspace ID")
    # id_dspace = forms.ChoiceField(choices=id_dspace_choices, label="Dspace ID")
    gsid = forms.MultipleChoiceField(choices=gs_choices, label="Google Service")

    def __init__(self, *args, **kwargs):
        return super(DspaceForm, self).__init__(*args, **kwargs)


class StatForm(forms.Form):
    PAGE_SIZE_CHOICES = (
        ('10', '10'),
        ('50', '50'),
        ('100', '100'),
        ('500', '500'),
        ('1000', '1000'),
    )
    gs_choices = Google_service.objects.all().values_list('id', 'name')
    period_choices = Period.objects.all().values_list('id', 'start_date')

    period = forms.MultipleChoiceField(choices=period_choices, label="Period")
    gsid = forms.MultipleChoiceField(choices=gs_choices, label="Google Service")
    pagesize = forms.ChoiceField(choices=PAGE_SIZE_CHOICES)
#     detail = forms.BooleanField(label="Detailed report", required=False)
    csv_output = forms.BooleanField(label="CSV Output", required=False)
    page = forms.IntegerField(label="Page", min_value=1)

    def __init__(self, *args, **kwargs):
        return super(StatForm, self).__init__(*args, **kwargs)
