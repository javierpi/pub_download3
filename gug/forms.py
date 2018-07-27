from django import forms
from gug.models import Google_service, Period, Publication

class ApplicationForm(forms.Form):
    PAGE_SIZE_CHOICES = (
        ('10', '10'),
        ('50', '50'),
        ('100', '100'),
        ('500', '500'),
        ('1000', '1000'),
    )
    # PAGE_CHOICES = Paginator.page_range
    gs_choices = Google_service.objects.all().values_list('id','name')
    period_choices = Period.objects.all().values_list('id','start_date')
    

    period = forms.MultipleChoiceField(choices=period_choices, label="Period")
    gsid = forms.MultipleChoiceField(choices=gs_choices, label="Google Service")
    pagesize = forms.ChoiceField(choices=PAGE_SIZE_CHOICES)
    detail = forms.BooleanField(help_text="Check for detailed report", label="Detailed report", required=False)
    page = forms.IntegerField(label="Page", min_value=1)

    def __init__(self, *args, **kwargs):
        paginator = getattr(self, 'paginator', None)
        if paginator:
            print('Paginatorrrr')
        #     self.fields['object_type'].widget.attrs['readonly'] = True

        return super(ApplicationForm, self).__init__(*args, **kwargs)

