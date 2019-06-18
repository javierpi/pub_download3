from apiclient.discovery import build
from google.oauth2 import service_account
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.core import management
from gug.models import Google_service, Period, Publication, Stats, Dspace, WorkArea, Extension
from datetime import datetime, timedelta, date
import json
import logging
########################################################
# python manage.py celery -A ansible3 worker -l info
########################################################

@shared_task
def get_titles():
    '''
        Obtiene titulos de las publicaciones que estan vacias.
        Las obtiene desde repositorio.cepal.org
    '''
    call_id = management.call_command(
        'get_title',
        verbosity=2)

def define_extension(filename):
    fileparts = filename.split(".")
    extension = ""
    if len(fileparts) > 1:
        extension = fileparts[-1]
        extension = extension[:9]

        if extension[0:3] == "pdf":
            extension = "pdf"
        # else:
        #     print(extension[0:3])    

        extension = extension.replace('#page=', '')
        extension = extension.replace('%3Bjse', '')
        extension = extension.replace('jsessi', '')
        extension = extension.replace('&amp;s', '')
        extension = extension.replace(';jsess', '')
        extension = extension.replace(';seque', '')
        extension = extension.replace(';jses', '')
        extension = extension.replace('&amp', '')
        extension = extension.replace('%20', '')
        extension = extension.replace(';La', '')
        extension = extension.replace(';js', '')
        extension = extension.replace(';El', '')
        extension = extension.replace(';j', '')            
        extension = extension.replace(';', '')            
        
    ext, created = Extension.objects.get_or_create(extension_chars=extension)
    return ext

def set_all_extension():
    pub_list = Publication.objects.all()
    for pub in pub_list:
        filename = pub.tfile
        ext = define_extension(filename)
        # pub.id_extension = None
        pub.id_extension = ext
        pub.save()


@shared_task
def get_GA(header=False):
    logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
    gservices = Google_service.objects.filter(active=True)
    periods = Period.objects.filter(active=True)
    for period in periods:
        start_date = str(period.start_date)
        end_date = str(period.end_date)
        for gs in gservices:
            max_prev = date.today() - timedelta(days=(gs.service.max_month_before*31))
            if max_prev > period.end_date or max_prev > period.start_date:
                # print(max_prev)
                print(gs.service.max_month_before)
                print('max_prev > period.end_date', max_prev, ' > ' , period.end_date)
                continue
            else:
                print('Obteniendo')

            scope = gs.scope
            discovery = (gs.discovery)
            secret_json = gs.secret_json
            client_secret_path = gs.client_secret_path
            service = str(gs.service)
            version = gs.version
            view_id = gs.view_id
            report = gs.report
            report = report.replace('view_id', view_id)
            report = report.replace('start_date', start_date)
            report = report.replace('end_date', end_date)
            report = json.loads(report)

            credentials = service_account.Credentials.from_service_account_file(client_secret_path, scopes=scope)
            if credentials is None:
                print("BAD CREDENTIALS")

            # delete all stats from this report
            delete_stat(gs, period)
            # raise

            if discovery:
                analytics = build(service, version, discoveryServiceUrl=discovery, cache_discovery=False)
                response = analytics.reports().batchGet(body=report).execute()
            else:
                analytics = build(service, version)
                response = analytics.searchanalytics().query(siteUrl=view_id, body=report).execute()

            if service == 'analytics':
                for report in response.get('reports', []):
                    columnHeader = report.get('columnHeader', {})
                    dimensionHeaders = columnHeader.get('dimensions', [])
                    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

                workareas = None
                for row in report.get('data', {}).get('rows', []):
                    dimensions = row.get('dimensions', [])
                    dateRangeValues = row.get('metrics', [])

                    for header, dimension in zip(dimensionHeaders, dimensions):
                        # print('Header=' + header + ': ' + dimension)
                        if header == 'ga:eventLabel':
                            url = dimension

                        if header == 'ga:pageTitle':
                            title = dimension

                        if header == 'ga:dimension1':
                            workareas = dimension

                    for i, values in enumerate(dateRangeValues):
                        for metricHeader, value in zip(metricHeaders, values.get('values')):
                            # print(metricHeader.get('name') + ': ' + value)
                            if metricHeader.get('name') == 'ga:totalEvents':
                                cantidad = value
                    save_record(gs, period, url, title, cantidad, workareas)
            elif service == 'webmasters':
                if 'rows' in response:
                    for row in response['rows']:
                        keys = ','.join(row['keys'])
                        output_row = [keys, row['clicks'], row['impressions'], row['ctr'], row['position']]
                        cantidad = row['clicks']
                        title = ''
                        url = keys
                        save_record(gs, period, url, title, cantidad, '')

            gs.last_update = datetime.now()
            gs.save()

        period.last_update = datetime.now()
        period.save()
        
    get_titles()

    check_periods()

def check_periods():
    import calendar
    ## Does this date have a period ??
    today = datetime.today()
    this_month = today.month
    this_year = today.year
    try:
        period = Period.objects.get(start_date__year=this_year, start_date__month = this_month)
    except Period.DoesNotExist:
        ## Create this new period
        firs_day, last_day = calendar.monthrange(this_year,this_month)
        p = Period(
            start_date = date(this_year, this_month, 1),
            end_date   = date(this_year, this_month, last_day),
            active     = True
            )
        p.save()

    ## Are other periods active ?
    periods = Period.objects.filter(active=True)
    for period in periods:
        start_date = str(period.start_date)
        end_date = str(period.end_date)
        max_prev = date.today() - timedelta(days=5)
        if max_prev > period.end_date :
            print('Closing period: ', period)
            period.active = False
            period.save()


def tospanish(workarea):
    if workarea == 'assuntos de gênero' or workarea == 'gender affairs' or workarea[:10] == 'asuntos de' or workarea[:9] == 'gender eq' or workarea[:10] == 'igualdad d' :
        return 'Asuntos de Género'
    elif workarea == 'comércio internacional e integração' or workarea == 'international trade and integration' or workarea[:10] == 'comercio i' or workarea[:15] == 'international t' :
        return 'Comercio internacional e integración'
    elif workarea == 'desenvolvimento econômico' or workarea[:5] == 'econo' or workarea == 'desar' or workarea == 'desa' or workarea[:7] == 'desarro':
        return 'Desarrollo económico'
    elif workarea == 'recursos naturais e infraestrutura' or workarea == 'natural resources and infrastructure' or workarea[:12] == 'natural reso' or workarea[:6] == 'recurs' :
        return 'Recursos naturales e infraestructura'    
    elif workarea == 'desenvolvimento social' or workarea == 'social development' or workarea[:4] == 'soci' :
        return 'Desarrollo Social'
    elif workarea == 'sustainable development and human settlements' or workarea == 'desenvolvimento sustentável e assentamentos humanos' or workarea[:15] == 'desenvolvimento' or workarea[:13] == 'sustainable d' or workarea[:14] == 'desarrollo sos':
        return 'Desarrollo sostenible y asentamientos humanos'
    elif workarea == 'planning for development' or workarea[:4] == 'plan'  or workarea[:12] == 'planning for' or workarea == 'planejamento para o desenvolvimento' :
        return 'Planificación para el desarrollo'
    elif workarea == 'statistics' or workarea == 'estatísticas' or workarea[:4] == 'esta' or workarea == 'statisti' or workarea == 'stat':
        return 'Estadísticas'    
    elif workarea == 'population and development' or workarea[:10] == 'population' or workarea[:10] == 'população ' or workarea[:6] == 'poblac' :
        return 'Población y desarrollo'    
    elif workarea == 'desenvolvimento produtivo e empresarial' or workarea == 'productivity and management' or workarea[:7] == 'product':
         return 'Desarrollo productivo y empresarial'    

    else:
        return workarea.capitalize()

def clean_url(n_url):
    n_url = n_url.split('?')[0]
    n_url = n_url.replace('http://', '')
    n_url = n_url.replace('https://', '')
    n_url = n_url.replace('repositorio.cepal.org', '')
    n_url = n_url.replace('/bitstream', '')
    n_url = n_url.replace('/handle', '')
    n_url = n_url.replace('/id/', '')
    n_url = n_url.replace('/11362/', '')
    return n_url

# @shared_task
def get_wa():
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    discovery = ('https://analyticsreporting.googleapis.com/$discovery/rest')
    client_secret_path = 'DownloadPublicaciones-a610ebc17b1e.json'
    service = 'analytics'
    version = 'v4'
    # 94626449
    # 94646409
    report = '{ "reportRequests": [ { "viewId": "94626449", "dateRanges": [{"startDate": "2017-01-01", "endDate": "2019-12-30"}], \
                            "metrics": [{"expression": "ga:totalEvents"}],"dimensions": [{"name": "ga:eventLabel"}, {"name": "ga:pageTitle"}, {"name": "ga:dimension1"}],"pageSize": 20000,"orderBys": [{"fieldName": "ga:totalEvents", "sortOrder": "DESCENDING"}], \
                            "dimensionFilterClauses": [{"operator": "AND"},{"filters": [{"dimensionName": "ga:eventLabel", "operator": "PARTIAL", "expressions": ["/bitstream/", ".pdf"] }]}] }]}'
    report = json.loads(report)
    credentials = service_account.Credentials.from_service_account_file(client_secret_path, scopes=scope)
    if credentials is None:
        print("BAD CREDENTIALS")

    # if discovery:
    analytics = build(service, version, discoveryServiceUrl=discovery, cache_discovery=False)
    response = analytics.reports().batchGet(body=report).execute()
   
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    workareas = None
    for row in report.get('data', {}).get('rows', []):
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])

        for header, dimension in zip(dimensionHeaders, dimensions):
            # print('Header=' + header + ': ' + dimension)
            if header == 'ga:eventLabel':
                url = dimension
            if header == 'ga:pageTitle':
                title = dimension
            if header == 'ga:dimension1':
                workareas = dimension
        # for i, values in enumerate(dateRangeValues):
        #     for metricHeader, value in zip(metricHeaders, values.get('values')):
        #         # print(metricHeader.get('name') + ': ' + value)
        #         if metricHeader.get('name') == 'ga:totalEvents':
        #             cantidad = value
        # save_record(gs, period, url, title, cantidad, workareas)
        n_url = clean_url(url)
        wka_list = []
        id_dspace = n_url.split("/")[0]

        for workarea in workareas.split(','):
            workarea = tospanish(workarea.strip().lower())
            if len(workarea) > 3:
                try:
                    wka = WorkArea.objects.get(name=workarea)
                except WorkArea.DoesNotExist:
                    wka = WorkArea(name=workarea)
                    wka.save()
                wka_list.append(wka)

        try:
            dsp = Dspace.objects.get(id_dspace=id_dspace)
        except ValueError:
            print('ValueError in id_dspace')
            print('url = ', url)
        except ObjectDoesNotExist:
            print('id_dspace Does Not Exist: ', id_dspace)

        else:
            dsp.workarea.set(wka_list)
            dsp.save()


def delete_stat(gs, period):
    print('deleting stats for period:', period, ' and gs:', gs)
    Stats.objects.filter(google_service=gs, period=period).delete()

def clean_title(title):
    ntitle = title
    ntitle = ntitle.replace('\\xF0', '')
    ntitle = ntitle.replace('\\x9F', '')
    ntitle = ntitle.replace('\\x8C', '')
    ntitle = ntitle.replace('\\x90', '')
    return ntitle
    

def save_record(gs, period, url, title, cantidad, workareas=None):
    #print(gs.id, period.id, url, title, cantidad)
    # n_url = url.split('?')[0]
    # n_url = n_url.replace('http://', '')
    # n_url = n_url.replace('https://', '')
    # n_url = n_url.replace('repositorio.cepal.org', '')
    # n_url = n_url.replace('/bitstream', '')
    # n_url = n_url.replace('/handle', '')
    # n_url = n_url.replace('/id/', '')
    # n_url = n_url.replace('/11362/', '')
    n_url = clean_url(url)

    id_dspace = n_url.split("/")[0]
    file = n_url.split("/")[-1]
    title = str(title)
    title = title[:599]
    title = clean_title(title)

    post_title1 = ''
    post_title2 = ''
    if title.count('|') == 2:
        post_title1 = title.split('|')[1]
    if title.count('|') == 3:
        post_title2 = title.split('|')[2]
    title = title.split('|')[0]

    if isNum(id_dspace) and int(cantidad) > 0:
        
        dsp, created = Dspace.objects.get_or_create(id_dspace=id_dspace)
        if len(title.strip()) > 0 :
            dsp.title = title
            dsp.post_title1 = post_title1
            dsp.post_title2 = post_title2
            dsp.save()

        ext = define_extension(file)

        try:
            pub = Publication.objects.get(id_dspace=dsp, tfile=file)
        except Publication.DoesNotExist:
            pub = Publication(id_dspace=dsp, tfile=file, id_extension=ext)
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


