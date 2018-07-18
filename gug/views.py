from apiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.urllib3 import AuthorizedHttp
from gug.models import Google_service, Period, Publication, Stats, Dspace
import json

def get_GCS(request):
    client_id = '1016686310199-sq9ujf1npoip452cjodgqptrrgcc1pke.apps.googleusercontent.com'
    client_secret = 'em10vMkwwVaPq4u6KOlv1MXa'
    # Custom Search API
    gcs_key = 'AIzaSyDL3FAKOL6xSCkv00UbR_cb_z28NXX1X3w'

    SCOPE_WEBMASTER = 'https://www.googleapis.com/auth/webmasters.readonly'
    # CLIENT_SECRETS_PATH = '/home/deployer/pub_download3/publications/DownloadPublicaciones-a610ebc17b1e.json'
    CLIENT_SECRETS_PATH = 'DownloadPublicaciones-a610ebc17b1e.json'

    # Redirect URI for installed apps
    REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
    property_uri = 'http://repositorio.cepal.org'

    credentials = service_account.Credentials.from_service_account_file(CLIENT_SECRETS_PATH, scopes=SCOPE_WEBMASTER)
    if credentials is None:
        print("BAD CREDENTIALS")

    authed_http = AuthorizedHttp(credentials)
    print(authed_http)

    service = build('webmasters', 'v3')
    
    output_rows = []

    request = {
        "startDate": "2018-06-01",
        "endDate": "2018-06-30",
        "dimensions": ["page"],
        "rowLimit": 20,
        "startRow": 0
        # 'dimensionFilterGroups' : [
        #     {
        #         "groupType" : "and",
        #         "filters" : filter_set
        #     }
        # ]
    }


    response = service.searchanalytics().query(siteUrl=property_uri, body=request).execute()


    if 'rows' in response:
        for row in response['rows']:
            keys = ','.join(row['keys'])
            output_row = [keys, row['clicks'], row['impressions'], row['ctr'], row['position']]
            print(output_row)
            # save_record(gs, period, url, title, cantidad)

    print(response)


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
            service = gs.service
            version = gs.version
            view_id = gs.view_id
            report = gs.report
            report = report.replace('view_id',view_id)
            report = report.replace('start_date',start_date)
            report = report.replace('end_date',end_date)
            report = json.loads(report)
            print(report)
            # VIEW_ID = '73365432'  # Todos los datos

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
                        # print('Date range: ' + str(i))
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
                        # print(url, title, cantidad)
                        save_record(gs, period, url, title, cantidad)
                        # print(output_row)
            # save_record(gs, period, url, title, cantidad)

        # print('response:', response)

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
    if isNum(id_dspace):
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



