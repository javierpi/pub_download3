from apiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.urllib3 import AuthorizedHttp
from gug.models import Google_service, Period, Publication, Stats, Dspace
import json
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Count, Sum, Min

class periods(ListView):
    context_object_name = 'periods'
    template_name = 'gug/periods_list.html'

    def get_queryset(self):
        #return Period.objects.all()
        return Period.objects.annotate(Count('stats'))
        #return Google_service.objects.annotate(Count('stats'))

    def get_context_data(self, **kwargs):
        context = super(periods, self).get_context_data(**kwargs)
#        context['statistics'] = Stats.objects.values('google_service').filter(period=self.get_object()).annotate(Count('cuantity'), Sum('cuantity')).order_by()
#        context['statistics'] = Stats.objects.values('period', 'period').filter(google_service=self.get_object()).annotate(Count('cuantity'), Sum('cuantity')).order_by()

        return context

class google_services_detail(DetailView):
    model = Google_service
    template_name = 'gug/google_service_detail.html'

    def get_context_data(self, **kwargs):
        context = super(google_services_detail, self).get_context_data(**kwargs)
        context['periods'] = Period.objects.all()
        context['statistics'] = Stats.objects.values('period').filter(google_service=self.get_object()).annotate(Count('cuantity'), Sum('cuantity')).order_by()
        return context

class google_services(ListView):
    context_object_name = 'google_service'
    template_name = 'gug/google_service.html'

    def get_queryset(self):
        return Google_service.objects.annotate(Count('stats'))

    def get_context_data(self, **kwargs):
        context = super(google_services, self).get_context_data(**kwargs)
#        context['servers_sums'] = Server.objects.filter(net_area__zone__in=myzones).aggregate(Sum('vcpu'), memory=Sum('memory') * 1024 * 1024)
        return context


def get_GCS(request):
    SCOPE_WEBMASTER = 'https://www.googleapis.com/auth/webmasters.readonly'
    CLIENT_SECRETS_PATH = 'DownloadPublicaciones-a610ebc17b1e.json'
    REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
    property_uri = 'http://repositorio.cepal.org'
    credentials = service_account.Credentials.from_service_account_file(CLIENT_SECRETS_PATH, scopes=SCOPE_WEBMASTER)
    if credentials is None:
        print("BAD CREDENTIALS")

    #authed_http = AuthorizedHttp(credentials)
    service = build('webmasters', 'v3')
    output_rows = []
    request = {
        "startDate": "2018-06-01",
        "endDate": "2018-06-30",
        "dimensions": ["page"],
        "searchType": "web",
        "rowLimit": 20000,
        "startRow": 0,
        "aggregationType": "byPage",
        "fileType": "pdf",
        "dimensionFilterGroups" : [
            {
                "filters" : [{
                    "dimension": "page",
                    "expression": "bitstream",
                    "operator": "contains"
                },
                {
                    "dimension": "page",
                    "expression": "pdf",
                    "operator": "contains"
                },
                {
                    "dimension": "page",
                    "expression": ".txt",
                    "operator": "notcontains"
                }
                ]
            }
        ]
    }
    response = service.searchanalytics().query(siteUrl=property_uri, body=request).execute()
    if 'rows' in response:
        row_count = 0
        for row in response['rows']:
            row_count = row_count + 1
            keys = ','.join(row['keys'])
            #output_row = [keys, row['clicks'], row['impressions'], row['ctr'], row['position']]
            output_row = [keys, row['clicks']]
            print(row_count, output_row)

    #print(response)


def get_GA(request):
    gservices = Google_service.objects.filter(active=True)
    periods = Period.objects.filter(active=True)
    for period in periods:
        start_date = str(period.start_date)
        end_date = str(period.end_date)

        for gs in gservices:
            scope = gs.scope
            discovery = (gs.discovery)
            secret_json = gs.secret_json
            client_secret_path = gs.client_secret_path
            service = str(gs.service)
            version = gs.version
            view_id = gs.view_id
            report = gs.report
            report = report.replace('view_id',view_id)
            report = report.replace('start_date',start_date)
            report = report.replace('end_date',end_date)
            report = json.loads(report)
            print(report)

            credentials = service_account.Credentials.from_service_account_file(client_secret_path, scopes=scope)
            if credentials is None:
                print("BAD CREDENTIALS")

            ## delete all stats from this report
            delete_stat(gs,period)
            if discovery:
            	analytics = build(service, version, discoveryServiceUrl=discovery)
            	response = analytics.reports().batchGet(body=report).execute()
            else: 
            	analytics = build(service, version)
            	response = analytics.searchanalytics().query(siteUrl=view_id, body=report).execute()
            
            if service == 'analytics':
                for report in response.get('reports', []):
                    columnHeader = report.get('columnHeader', {})
                    dimensionHeaders = columnHeader.get('dimensions', [])
                    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

                for row in report.get('data', {}).get('rows', []):
                    dimensions = row.get('dimensions', [])
                    dateRangeValues = row.get('metrics', [])

                    for header, dimension in zip(dimensionHeaders, dimensions):
                        # print('H%D=' + header + ': ' + dimension)
                        if header == 'ga:eventLabel':
                            url = dimension

                        if header == 'ga:pageTitle':
                            title = dimension

                    for i, values in enumerate(dateRangeValues):
                        for metricHeader, value in zip(metricHeaders, values.get('values')):
                            # print(metricHeader.get('name') + ': ' + value)
                            if metricHeader.get('name') == 'ga:totalEvents':
                                cantidad = value
                    save_record(gs, period, url, title, cantidad)
            elif service == 'webmasters':
                if 'rows' in response:
                    for row in response['rows']:
                        keys = ','.join(row['keys'])
                        output_row = [keys, row['clicks'], row['impressions'], row['ctr'], row['position']]
                        cantidad = row['clicks']
                        title = ''
                        url = keys
                        save_record(gs, period, url, title, cantidad)
                        # print(output_row)

def delete_stat(gs,period):
	Stats.objects.filter(google_service=gs, period=period).delete()

def save_record(gs, period, url, title, cantidad):
    #print(gs.id, period.id, url, title, cantidad)
    n_url = url.split('?')[0]
    n_url = n_url.replace('http://','')
    n_url = n_url.replace('https://','')
    n_url = n_url.replace('repositorio.cepal.org','')
    n_url = n_url.replace('/bitstream','')
    n_url = n_url.replace('/handle','')
    n_url = n_url.replace('/id/','')
    n_url = n_url.replace('/11362/','')
    
    id_dspace = n_url.split("/")[0]
    file = n_url.split("/")[-1]
    title = title[:599]

    print(url, n_url, id_dspace, file)
    if isNum(id_dspace) and int(cantidad) > 0:
        # dsp, created = Dspace.objects.get_or_create(id_dspace=id_dspace, title=title)
        try:
            dsp = Dspace.objects.get(id_dspace=id_dspace)
        except Dspace.DoesNotExist:
            dsp = Dspace(id_dspace=id_dspace, title=title)
            dsp.save()


        try:
            pub = Publication.objects.get(id_dspace=dsp, tfile=file)
        except Publication.DoesNotExist:
            pub = Publication(id_dspace=dsp, tfile=file)
            pub.save()

        try:
            stat = Stats.objects.get(google_service=gs, period=period, publication=pub, id_dspace=dsp)
            can = stat.cuantity + int(cantidad)
            stat.cuantity = can
            stat.save()
        except Stats.DoesNotExist:
            stats = Stats(google_service=gs, period=period, publication=pub, id_dspace=dsp, cuantity=cantidad)
            stats.save()


def isNum(data):
    try:
        int(data)
        return True
    except ValueError:
        return False



