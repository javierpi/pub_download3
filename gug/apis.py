import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
# from django.http import HttpResponse, , JsonResponse, HttpResponseNotFound


from django.http import JsonResponse, StreamingHttpResponse
from django.db.models import Count, Sum
from django.db import connection
from gug.models import Google_service, Period, Publication, Stats, Dspace, Service_group
import gviz_api
import csv
import codecs

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def iter_csv(rows, pseudo_buffer):
    yield pseudo_buffer.write(codecs.BOM_UTF8)
    writer = csv.writer(pseudo_buffer)
    for row in rows:
        yield writer.writerow(row)

# @api_view(['GET'])
class get_report(APIView):
    authentication_classes = []
    permission_classes = []

    # def __init__(self, request, period, output):
    #     pass

    def get(self, request, *args, **kwargs):
        period = request.GET.get('period', '1')
        output = request.GET.get('output', 'json')  ## json; csv; gvdtj (Google Visualization Data Table JSON)

        gsid_avalable = list(Google_service.objects.values_list('id', flat=True))
        gsid = []
        for x in gsid_avalable:
            gsid.append(str(x))

        #### --    BY GROUP ----
        ## group headers
        # gstitles = Google_service.objects.values('group__id', 'group__name').annotate(dcount=Count('group__id'))
        gstitles = Service_group.objects.values('id', 'name').annotate(dcount=Count('id'))

        fields_iniciales = ['ID Dspace', 'Title', 'Work Area']
        fields = []
        for title in fields_iniciales:
            fields.append(title)
        
        columns_order = []
        columns_order.append('id_dspace')
        columns_order.append('title')
        columns_order.append('wa')

        fields2 = []
        fields2.append({'id_dspace': ("number", "ID DSpace")})
        fields2.append({'title': ("string", "Title")})
        fields2.append({'wa': ("string", "Work Area")})
        for title in gstitles:
            fields.append(title['name'] )
            columns_order.append('group_' + str(title['id'])  )
            # fields2.append({'group_' + str(title['group__id']) : ("number", title['group__name'])})
            fields2.append({'group_' + str(title['id']) : ("number", title['name'])})
        fields_finales = ['SUMA']
        fields.append(','.join(map(str, fields_finales)))


        columns_order.append('suma')
        fields2.append({'suma': ("number", "SUMA")})

        #
        # groupid_avalable = list(Google_service.objects.select_related('group').filter(pk__in=gsid).values_list('group_id', flat=True).distinct())
        groupid_avalable = list(Service_group.objects.values_list('id', flat=True))
        

        groupids = []
        for x in groupid_avalable:
            groupids.append(str(x))
        
        ## group resumes
        query_inicial = " SELECT " \
                        "       gug_dspace.id_dspace, "\
                        "       gug_dspace.title ,  "\
                        "       ("\
                        "           SELECT GROUP_CONCAT(gug_workarea.name SEPARATOR ', ')"\
                        "           FROM gug_dspace_workarea inner join gug_workarea "\
                        "               on gug_dspace_workarea.workarea_id = gug_workarea.id "\
                        "           WHERE gug_dspace_workarea.dspace_id = gs_master.id_dspace_id "\
                        "           GROUP BY dspace_id "\
                        "       ) as areasdetrabajo,"
        query_rows = ""
        query_final = "         , sum(cuantity) as sumtotal "\
                      "  FROM gug_stats as gs_master "\
                      "  INNER join gug_dspace " \
                      "     on gs_master.id_dspace_id = gug_dspace.id" \
                      "  INNER join gug_google_service " \
                      "     on gs_master.google_service_id = gug_google_service.id "\
                      "  WHERE "\
                      "        gug_google_service.group_id in (" + ','.join(groupids) + ") and " \
                      "        period_id = " + period + " " \
                      "  GROUP by id_dspace_id"\
                      "  ORDER by sumtotal desc "

        num_cols = 0
        for groupn in groupids:
            gsid2 = list(Google_service.objects.filter(group_id=groupn, pk__in=gsid).values_list('id', flat=True).distinct())
            groupids2 = []
            for x in gsid2:
                groupids2.append(str(x))

            num_cols += 1
            sumvar = "sumags" + str(num_cols)
            # scolvar = "colags" + str(num_cols)
            fromvar = "gs" + str(num_cols)
            query_rows += " ( SELECT "\
                          "     sum(cuantity) as " + sumvar + " "\
                          "   FROM gug_stats as " + fromvar + " " \
                          "   WHERE "\
                          "     google_service_id in (" + ','.join(groupids2) + ") and " \
                          "     period_id = " + period + " and "\
                          "     gs_master.id_dspace_id = " + fromvar + ".id_dspace_id "\
                          "   GROUP by id_dspace_id "\
                          " ) AS '" + sumvar + "' ,"
        final_sql = query_inicial + query_rows[:-1] + query_final


        print(final_sql)
        cursor = connection.cursor()
        cursor.execute(final_sql)
        stats = cursor.fetchall()
        if output == 'csv':
            rows = []
            row = []
            colcount = 0
            for head in fields:
                row.append(head)
            rows.append(row)

            for stat in stats:
                row = []
                ## Columnas iniciales del Encabezado
                for col in list(range(0, len(fields_iniciales))):
                    line = str(stat[col])
                    line = line.replace('\n', ' ')
                    line = line.replace('\r', ' ')
                    row.append(line )
                
                ## Columnas con nombres de grupo y columnas finales
                for col in list(range(len(fields_iniciales), (len(fields_iniciales) + len(groupids) + len(fields_finales)))):
                    if stat[col] is None:
                        valor = 0
                    else:
                        valor = int(stat[col])
                    row.append(valor)
                rows.append(row)
                

            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer)
            response = StreamingHttpResponse(iter_csv(rows, Echo()), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="get_report-id_period_' + period + '.csv"'

            return response
        elif output == 'gvdtj':
            data = []
            for stat in stats:
                row = []
                for col in list(range(0, len(fields2))):
                    head_values = list(fields2[col].values())
                    head_name = list(fields2[col])[0]
                    head_type = head_values[0][0]
                    if head_type == 'string':
                        row.append({head_name: str(stat[col]) })
                    elif head_type == 'number':
                        if stat[col] is None:
                            valor = 0
                        else:
                            valor = int(stat[col])
                        row.append(valor)
                        row.append({head_name: valor })

                data.append(row)

                # if stat[6] is None:
                #     val4 = 0
                # else:
                #     val4 = int(stat[6])
                # data.append({"id_dspace": stat[0], "title": stat[1], "wa": stat[2],"group_1": val1 ,"group_2": val2, "group_3": val3, "group_4": val4, "suma": val_suma })

            data_table = gviz_api.DataTable(fields2.items())
            
            data_table.LoadData(data)
            string_order = ','.join(map(str, columns_order))
            # Create a JSON string.
            json2 = data_table.ToJSon(columns_order=(columns_order))
            python_obj = json.loads(json2)

            return JsonResponse(python_obj, safe=False)
        elif output == 'json':
            return JsonResponse(stats, safe=False)


 
class get_data(APIView):
    authentication_classes = []
    permission_classes = []
    # def get(self, request, dspace_id, gsid, *args, **kwargs):

    def get(self, request, *args, **kwargs):
        gsid = request.GET.getlist('gsid', 1)
        id_dspace = request.GET.get('id_dspace', 1)
        gs = Google_service.objects.filter(pk__in=gsid)
        detail = request.GET.get('detail', 'off')
        period = request.GET.getlist('period', 1)
        by = request.GET.get('by', '')
        if by == 'file':
            query_final = "select "\
                " gug_publication.tfile, "\
                " sum(cuantity) as sumtotal "\
                " from gug_stats as gs_master "\
                " inner join gug_publication ON gs_master.publication_id = gug_publication.id  "\
                " inner join gug_dspace ON gs_master.id_dspace_id = gug_dspace.id  "\
                " inner join gug_period ON gs_master.period_id = gug_period.id  "\
                " where "\
                " gs_master.google_service_id in (" + ','.join(gsid) + ") " \
                " and gs_master.period_id in (" + ','.join(period) + ") " \
                " and gug_dspace.id_dspace = " + str(id_dspace) + "" \
                " group by "\
                " gug_publication.tfile"\
                " order by gug_publication.tfile asc;"
        else:
            query_final = "select gug_period.start_date, sum(cuantity) as sumtotal from gug_stats as gs_master"\
                " inner join gug_dspace ON gs_master.id_dspace_id = gug_dspace.id " \
                " inner join gug_period ON gs_master.period_id = gug_period.id " \
                " where gs_master.google_service_id in (" + ','.join(gsid) + ") and "\
                " gs_master.period_id in (" + ','.join(period) + ") and "\
                " gug_dspace.id_dspace = " + str(id_dspace) + "  "\
                " group by period_id " \
                " order by gug_period.start_date asc "
        # dspace_id = int(dspace_id)
        # gsid = request.GET.getlist('gsid', 1)
        if detail == 'on':
            query_final = "select gug_period.start_date, gug_publication.tfile, sum(cuantity) as sumtotal from gug_stats as gs_master"\
                " inner join gug_publication on gs_master.publication_id = gug_publication.id "\
                " inner join gug_dspace ON gs_master.id_dspace_id = gug_dspace.id " \
                " inner join gug_period ON gs_master.period_id = gug_period.id " \
                " where gs_master.google_service_id in (" + ','.join(gsid) + ") and "\
                " gs_master.period_id in (" + ','.join(period) + ") and "\
                " gug_dspace.id_dspace = " + str(id_dspace) + "  "\
                " group by gug_publication.tfile, period_id " \
                " order by gug_publication.tfile, gug_period.start_date asc "

        # print(query_final)
        cursor = connection.cursor()
        cursor.execute(query_final)
        stats = cursor.fetchall()
        data = []
        for stat in stats:
            if detail == 'on':
                data.append({"period": stat[0], "file": stat[1], "cuantity": int(stat[2])})
                fields_description = {"period": ("date", "Period"),
                                      "file": ("string", "File"),
                                      "cuantity": ("number", "Downloads")}
            if by == 'file':
                data.append({"file": stat[0], "cuantity": int(stat[1])})
                fields_description = {"file": ("string", "File"),
                                      "cuantity": ("number", "Downloads")}
            else:
                data.append({"period": stat[0], "cuantity": int(stat[1])})
                fields_description = {"period": ("date", "Period"),
                                      "cuantity": ("number", "Downloads")}

        # data_table = gviz_api.DataTable(description)
        data_table = gviz_api.DataTable(fields_description)
        data_table.LoadData(data)

        # Create a JSON string.
        if detail == 'on':
            json2 = data_table.ToJSon(columns_order=("period", "file", "cuantity"), order_by="file")
        if by == 'file':
            json2 = data_table.ToJSon(columns_order=("file", "cuantity"), order_by="file")
        else:
            json2 = data_table.ToJSon(columns_order=("period", "cuantity"), order_by="period")

        python_obj = json.loads(json2)

        return JsonResponse(python_obj, safe=False)
