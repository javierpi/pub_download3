import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db import connection
from gug.models import Google_service, Period, Publication, Stats, Dspace
import gviz_api


class get_report(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        period = request.GET.get('period', 1)
        gsid_avalable = list(Google_service.objects.values_list('id', flat=True))
        gsid = []
        for x in gsid_avalable:
            gsid.append(str(x))
        # gsid = request.GET.getlist('gsid', gs_list)

        #### --    BY GROUP ----
        ## group headers
        gstitles = Google_service.objects.values('group', 'group__name').filter(pk__in=gsid).annotate(dcount=Count('group'))
        fields2 = ['Period']
        for title in gstitles:
            fields2.append(title)
        fields2.append('Total Downloads')
        #
        groupid_avalable = list(Google_service.objects.select_related('group').filter(pk__in=gsid).values_list('group_id', flat=True).distinct())
        group_list = []
        for x in groupid_avalable:
            group_list.append(str(x))
        groupids = group_list
        ## group resumes
        group_query_resume_inicial = "select  'Total' as tit1, "
        group_query_resume_rows = ""
        group_query_resume_final = ", sum(cuantity) as sumtotal " \
                            " from gug_stats as gs_master " \
                            " inner join gug_dspace on gs_master.id_dspace_id = gug_dspace.id "\
                            " inner join gug_google_service on gs_master.google_service_id = gug_google_service.id " \
                            " where gug_google_service.group_id in (" + ','.join(groupids) + ") " \
                            " and gs_master.google_service_id in (" + ','.join(gsid) + ") " \

        group_query_resume_final += " and period_id = " + period + " "
        #

        group_query_inicial = "select gug_period.start_date , "
        group_query_rows = ""
        group_query_final = ", sum(cuantity) as sumtotal from gug_stats as gs_master " \
                    " inner join gug_dspace on gs_master.id_dspace_id = gug_dspace.id "\
                    " inner join gug_period on gs_master.period_id = gug_period.id  " \
                    " inner join gug_google_service on gs_master.google_service_id = gug_google_service.id " \
                    " where gs_master.google_service_id in (" + ','.join(gsid) + ") " \
                    " and period_id = " + period + " " \
                    " group by gs_master.period_id order by gug_period.start_date desc "
        # " and period_id in (" + ','.join(period) + ") " \
        num_cols = 0
        google_services_groups = []
        for groupn in groupids:
            gsid2 = list(Google_service.objects.filter(group_id=groupn, pk__in=gsid).values_list('id', flat=True).distinct())
            group_list2 = []
            for x in gsid2:
                group_list2.append(str(x))
            groupids2 = group_list2

            gstitles = Google_service.objects.filter(group_id=groupn, pk__in=gsid)
            fields = ['Period']
            for title in gstitles:
                fields.append(title.name.split(' '))
            fields.append('Total Downloads')

            num_cols += 1
            sumvar = "sumags" + str(num_cols)
            scolvar = "colags" + str(num_cols)
            fromvar = "gs" + str(num_cols)
            group_query_rows += "(select sum(cuantity)  as " + sumvar + " " \
                        " from gug_stats as " + fromvar + "" \
                        " inner join gug_dspace on " + fromvar + ".id_dspace_id = gug_dspace.id  " \
                        " where google_service_id in (" + ','.join(groupids2) + ") " \
                        " and period_id =  gs_master.period_id " \
                        " ) AS '" + sumvar + "' ,"

        group_sql = group_query_inicial + group_query_rows[:-1] + group_query_final 

        print(group_sql)
        cursor = connection.cursor()
        cursor.execute(group_sql)
        stats = cursor.fetchall()
        data = []
        for stat in stats:
            data.append({"period": stat[0], "cuantity": int(stat[1])})
            fields_description = {"period": ("date", "Period"),
                                  "cuantity": ("number", "Downloads")}

        # data_table = gviz_api.DataTable(description)
        data_table = gviz_api.DataTable(fields_description)
        data_table.LoadData(data)

        # Create a JSON string.
        json2 = data_table.ToJSon(columns_order=("period", "cuantity"), order_by="period")

        python_obj = json.loads(json2)

        return JsonResponse(python_obj, safe=False)

 
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
