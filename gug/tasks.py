from apiclient.discovery import build
from google.oauth2 import service_account
from celery import shared_task
from gug.models import Google_service, Period, Publication, Stats, Dspace, WorkArea
from datetime import datetime
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
        verbosity=2,
        interactive=False)
    return_vars = json.loads(str(call_id))


@shared_task
def get_GA(header=False):
    logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
    gservices = Google_service.objects.filter(active=True)
    periods = Period.objects.filter(active=True)
    for period in periods:
        start_date = str(period.start_date)
        end_date = str(period.end_date)
        period.last_update = datetime.now()
        period.save()

        for gs in gservices:
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
            # print(report)

            credentials = service_account.Credentials.from_service_account_file(client_secret_path, scopes=scope)
            if credentials is None:
                print("BAD CREDENTIALS")

            # delete all stats from this report

            delete_stat(gs, period)
            gs.last_update = datetime.now()
            gs.save()
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
                        # print(output_row)
       


def delete_stat(gs, period):
    print('deleting stats for period:', period, ' and gs:', gs)
    Stats.objects.filter(google_service=gs, period=period).delete()


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
    
    
def save_record(gs, period, url, title, cantidad, workareas=None):
    #print(gs.id, period.id, url, title, cantidad)
    n_url = url.split('?')[0]
    n_url = n_url.replace('http://', '')
    n_url = n_url.replace('https://', '')
    n_url = n_url.replace('repositorio.cepal.org', '')
    n_url = n_url.replace('/bitstream', '')
    n_url = n_url.replace('/handle', '')
    n_url = n_url.replace('/id/', '')
    n_url = n_url.replace('/11362/', '')

    id_dspace = n_url.split("/")[0]
    file = n_url.split("/")[-1]
    title = title[:599]
    post_title1 = ''
    post_title2 = ''
    if title.count('|') == 2:
        post_title1 = title.split('|')[1]
    if title.count('|') == 3:
        post_title2 = title.split('|')[2]
    title = title.split('|')[0]

    if isNum(id_dspace) and int(cantidad) > 0:
        wka_list = []
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
            dsp, created = Dspace.objects.update_or_create(
                    id_dspace=id_dspace,
                    defaults={
                        'title': title,
                        'post_title1': post_title1,
                        'post_title2': post_title2
                        }
                    )
        except:
            print('OperationalError')
        else:
            dsp.workarea.set(wka_list)

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


