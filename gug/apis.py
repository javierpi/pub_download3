import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db import connection
from gug.models import Google_service, Period, Publication, Stats, Dspace
import gviz_api



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
        else:
            query_final = "select gug_period.start_date, sum(cuantity) as sumtotal from gug_stats as gs_master"\
                " inner join gug_dspace ON gs_master.id_dspace_id = gug_dspace.id " \
                " inner join gug_period ON gs_master.period_id = gug_period.id " \
                " where gs_master.google_service_id in (" + ','.join(gsid) + ") and "\
                " gs_master.period_id in (" + ','.join(period) + ") and "\
                " gug_dspace.id_dspace = " + str(id_dspace) + "  "\
                " group by period_id " \
                " order by gug_period.start_date asc "
            
            # select gug_period.start_date, gug_publication.tfile, sum(cuantity) as sumtotal from gug_stats as gs_master inner join gug_publication on gs_master.publication_id = gug_publication.id inner join gug_dspace ON gs_master.id_dspace_id = gug_dspace.id  inner join gug_period ON gs_master.period_id = gug_period.id  where gs_master.google_service_id in (4) and  gs_master.period_id in (18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,19,20) and  gug_dspace.id_dspace = 42001   group by gug_publication.tfile, period_id  order by gug_period.start_date asc;

        print(query_final)
        cursor = connection.cursor()
        cursor.execute(query_final)
        stats = cursor.fetchall()
        data = []
        for stat in stats:
            if detail == 'on':
                data.append({"period" : stat[0], "file": stat[1], "cuantity": int(stat[2]) })
                fields_description = {"period": ("date", "Period"),
                             "file": ("string", "File"),
                             "cuantity": ("number", "Downloads")}
            else:
                data.append({"period" : stat[0], "cuantity": int(stat[1]) })
                fields_description = {"period": ("date", "Period"),
                             "cuantity": ("number", "Downloads")}


        


        # data_table = gviz_api.DataTable(description)
        data_table = gviz_api.DataTable(fields_description)
        data_table.LoadData(data)

        # Create a JSON string.
        if detail == 'on':
            json2 = data_table.ToJSon(columns_order=("period", "file", "cuantity"), order_by="file")
        else:
            json2 = data_table.ToJSon(columns_order=("period", "cuantity"), order_by="period")
 
        python_obj = json.loads(json2)

        return JsonResponse(python_obj, safe=False)

