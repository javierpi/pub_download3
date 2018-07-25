from django import forms
from gug.models import Google_service, Period, Publication

class AWS_VMCopyForm(forms.Form):
    hypervisor = forms.ChoiceField(choices=[], label="Hypervisor")

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(AWS_VMCopyForm, self).__init__(*args, **kwargs)
        for key, value in extra.items():
            self.fields['customfield.%s' % key] = forms.CharField(label=key, initial=value)


class AWS_VMCopyForm2(forms.Form):
    hostname = forms.CharField(label="Hostname")
    vcp_id = forms.ChoiceField(choices=[])
    network = forms.ChoiceField(choices=[])
    ami = forms.ChoiceField(choices=[], help_text="", label="AMI")
    cluster = forms.CharField(help_text="", label="Cluster")

    server_type = forms.CharField(help_text="", label="Server Type")

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(AWS_VMCopyForm2, self).__init__(*args, **kwargs)

        for key, value in extra.items():
            self.fields['customfield.%s' % key] = forms.CharField(label=key, initial=value)


class VMCreateForm(forms.Form):
    hostname = forms.CharField(label="Hostname")
    domain = forms.CharField(label="Domain")
    description = forms.CharField(help_text="Please provide a detailed description")

  #  template = forms.ChoiceField(choices=[])

    # Memory has to be in KB
    MEMORY_CHOICES = (
        ('268435456', '256 MB'),
        ('536870912', '512 MB'),
        ('1073741824', '1 GB'),
        ('2147483648', '2 GB'),
        ('4294967296', '4 GB'),
        ('6442450944', '6 GB'),
        ('8589934592', '8 GB'),
        ('10737418240', '10 GB'),
        ('12884901888', '12 GB'),
        ('15032385536', '14 GB'),
        ('17179869184', '16 GB'),
    )

    CPU_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('4', '4'),
        ('6', '6'),
        ('8', '8'),
        ('10', '10'),
        ('12', '12'),
        ('14', '14'),
        ('16', '16'),
    )
    mem_size = forms.ChoiceField(choices=MEMORY_CHOICES, initial='512', label="Memory Size")
    cpu_cores = forms.ChoiceField(choices=CPU_CHOICES, initial='1', label="CPU Cores", help_text="<br />")

    network = forms.ChoiceField(choices=[])
    ip_address = forms.GenericIPAddressField(protocol='ipv4', label="IPv4 Address")
    ip_address6 = forms.GenericIPAddressField(protocol='ipv6', required=False, label="IPv6 Address (optional)")

    host = forms.ChoiceField(choices=[])
    backup = forms.BooleanField(label="Create Backups using XenBackup", required=False, help_text="Check to enable a daily backup of this VM")

    password = forms.CharField(help_text="Save the password! It will not be shown again!")
    sshkey = forms.CharField(help_text="Public Key in OpenSSH format", label="SSH key")

    tags = forms.MultipleChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(VMCreateForm, self).__init__(*args, **kwargs)

        for key, value in extra.items():
            self.fields['customfield.%s' % key] = forms.CharField(label=key, initial=value)




class VMEditForm(forms.Form):
    description = forms.CharField(help_text="Please provide a detailed description", label="Description")
    mem_size = forms.IntegerField(label="Memory Size", help_text="Size in MB (Only editable if VM is Halted)", min_value=256)
    cpu_cores = forms.IntegerField(label="CPU Cores", help_text="(Only editable if VM is Halted)", initial=1, min_value=1)
    backup = forms.BooleanField(help_text="Select if we should create Backups for this VM", label="Create Backups", required=False)
    tags = forms.MultipleChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(VMEditForm, self).__init__(*args, **kwargs)

        for key, value in extra.items():
            self.fields['customfield.%s' % key] = forms.CharField(label=key, initial=value)


class NetworkEditForm(forms.Form):
    name = forms.CharField(help_text="Please provide a name")
    description = forms.CharField(help_text="Please provide a detailed description")


class TagsForm(forms.Form):
    tags = forms.MultipleChoiceField(choices=[])


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

