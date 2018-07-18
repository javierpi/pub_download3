from apiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.urllib3 import AuthorizedHttp
from gug.models import Google_service, Period, Publication, Stats


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

# Authenticate and construct service.
    # http = httplib2.Http()
    # http = credentials.authorize(http)

    # service = build('webmasters', 'v3', http=http_auth)
    # service = build('webmasters', 'v3', http=authed_http)
    service = build('webmasters', 'v3')
    start_date = datetime.strptime('2018-06-01', "%Y-%m-%d")
    end_date = datetime.strptime('2018-06-30', "%Y-%m-%d")

    output_rows = []

    request = {
        'startDate': '2018-06-01',
        'endDate': '2018-06-30',
        'dimensions': ['query'],
        'rowLimit': 20,
        # 'dimensionFilterGroups' : [
        #     {
        #         "groupType" : "and",
        #         "filters" : filter_set
        #     }
        # ]
    }
    response = service.sites().list().execute()
    print(response)

    # response = service.searchanalytics().query(siteUrl=property_uri, body=request).execute()

    if 'rows' in response:
        for row in response['rows']:
            keys = ','.join(row['keys'])
            output_row = [keys, row['clicks'], row['impressions'], row['ctr'], row['position']]
            print(output_row)
            # output_row.extend(filters)
            # output_rows.append(output_row)


def get_GA(request):
    gservices = Google_service.objects.all()
    period = Period.objects.get(pk=1)
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
        # VIEW_ID = '73365432'  # Todos los datos

        credentials = service_account.Credentials.from_service_account_file(client_secret_path, scopes=scope)
        if credentials is None:
            print("BAD CREDENTIALS")

        analytics = build(service, version, discoveryServiceUrl=discovery)

        response = analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': view_id,
                        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                        'metrics': [{'expression': 'ga:totalEvents'}],
                        'dimensions': [{'name': 'ga:eventLabel'}, {'name': 'ga:pageTitle'}],
                        'pageSize': 1700,
                        'orderBys': [
                            {
                                "fieldName": "ga:totalEvents",
                                "sortOrder": "DESCENDING"
                            }],
                        'dimensionFilterClauses': [
                            {"operator": "AND"},
                            {"filters": [
                                {"dimensionName": 'ga:eventLabel', "operator": 'REGEXP', "expressions": ['/bitstream/', '.pdf'], }
                            ]}
                        ]
                    }]
            }
        ).execute()

        row_count = 0
        for report in response.get('reports', []):
            columnHeader = report.get('columnHeader', {})
            dimensionHeaders = columnHeader.get('dimensions', [])
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            # print('row_count:', row_count)
            row_count = row_count + 1
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
            # print('---')

        # print('response:', response)


def save_record(gs, period, url, title, cantidad):
    # print(gs.id, period.id, url, title, cantidad)
    try:
        pub = Publication.objects.get(turl=url, title=title)
    except Publication.DoesNotExist:
        pub = Publication(turl=url, title=title)
        pub.save()

    obj, created = Stats.objects.update_or_create(
        google_service=gs,
        period=period,
        publication=pub,
        cuantity=cantidad
        # defaults={'first_name': 'Bob'},
    )


def get_GA2(request):
    # client_id = '1016686310199-sq9ujf1npoip452cjodgqptrrgcc1pke.apps.googleusercontent.com'
    # client_secret = 'em10vMkwwVaPq4u6KOlv1MXa'
    # ## Custom Search API
    # gcs_key = 'AIzaSyDL3FAKOL6xSCkv00UbR_cb_z28NXX1X3w'

    SCOPE_ANALYTICS = 'https://www.googleapis.com/auth/analytics.readonly'
    DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
    CLIENT_SECRETS_PATH = 'DownloadPublicaciones-a610ebc17b1e.json'

    # Redirect URI for installed apps
    # REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
    # VIEW_ID = '119430816' ## www+repositorio
    VIEW_ID = '73365432'  # Todos los datos

    credentials = service_account.Credentials.from_service_account_file(CLIENT_SECRETS_PATH, scopes=SCOPE_ANALYTICS)
    if credentials is None:
        print("BAD CREDENTIALS")

# Authenticate and construct service.
    analytics = build('analytics', 'v4', discoveryServiceUrl=DISCOVERY_URI)
    # # Build the service object.
    # analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

    response = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '2018-06-01', 'endDate': '2018-06-30'}],
                    'metrics': [{'expression': 'ga:totalEvents'}, {'expression': 'ga:uniqueEvents'}],
                    'dimensions': [{'name': 'ga:eventLabel'}, {'name': 'ga:pageTitle'}],
                    'pageSize': 5,
                    'orderBys': [
                        {
                            "fieldName": "ga:totalEvents",
                            "sortOrder": "DESCENDING"
                        }],
                    'dimensionFilterClauses': [
                        {"operator": "AND"},
                        {"filters": [
                            {"dimensionName": 'ga:eventLabel', "operator": 'REGEXP', "expressions": ['/bitstream/', '.pdf'], }
                        ]}
                    ]
                }]
        }
    ).execute()

    row_count = 0
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
        print('row_count:', row_count)
        row_count = row_count + 1
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])

        for header, dimension in zip(dimensionHeaders, dimensions):
            print(header + ': ' + dimension)

        for i, values in enumerate(dateRangeValues):
            print('Date range: ' + str(i))
            for metricHeader, value in zip(metricHeaders, values.get('values')):
                print(metricHeader.get('name') + ': ' + value)
        print('---')
