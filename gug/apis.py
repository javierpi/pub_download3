import json
from rest_framework.views import APIView
from rest_framework.response import Response

from gug.models import Google_service, Period, Publication, Stats, Dspace
import gviz_api


# def get_data(request):
#     description = {"name": ("string", "Name"),
#                    "salary": ("number", "Salary"),
#                    "full_time": ("boolean", "Full Time Employee")}
#     data = [{"name": "Mike", "salary": (10000, "$10,000"), "full_time": True},
#             {"name": "Jim", "salary": (800, "$800"), "full_time": False},
#             {"name": "Alice", "salary": (12500, "$12,500"), "full_time": True},
#             {"name": "Bob", "salary": (7000, "$7,000"), "full_time": True}]

#     data_table = gviz_api.DataTable(description)
#     data_table.LoadData(data)
#     mijson = data_table.ToJSonResponse(columns_order=("name", "salary", "full_time"),
#                                        order_by="salary")

#     mijson += data_table.ToJSonResponse(columns_order=("name", "salary", "full_time"),
#                                         order_by="salary")
#     # return http.HttpResponse(mijson)
#     return JsonResponse(description, safe=False)


class get_data(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk, ctype, *args, **kwargs):
        testid = int(pk)
        title = Period.objects.get(pk=testid)
        series = []
        # tstamps = TestResult.objects.filter(test=testid).order_by("timestamp").values_list("timestamp", flat=True).distinct()
        # # Set unique dates
        # category_list = []
        # first = True
        # for tstamp in tstamps:
        #     if first:
        #         first = False
        #         fdate = tstamp.date().strftime('%d-%m-%y') + ' ' + tstamp.time().strftime('%H:%M')
        #         category_list.append(fdate)
        #     if fdate != tstamp.date().strftime('%d-%m-%y') + ' ' + tstamp.time().strftime('%H:%M'):
        #         fdate = tstamp.date().strftime('%d-%m-%y') + ' ' + tstamp.time().strftime('%H:%M')
        #         category_list.append(fdate)

        # hosts = TestResult.objects.all().filter(test=testid).order_by("serverhostname").values("serverhostname", "documentpath").distinct()
        # for host in hosts:
        #     results = TestResult.objects.all().filter(test=testid, serverhostname=host['serverhostname'], documentpath=host['documentpath'])
        #     dataperhost = []
        #     for result in results:
        #         dataperhost.append(round(result.timetakenfortests, 2))
        #     series.append({'name': host['serverhostname'] + host['documentpath'], "data": dataperhost})
        description = {"name": ("string", "Name"),
                       "salary": ("number", "Salary"),
                       "full_time": ("boolean", "Full Time Employee")}
        data = [{"name": "Mike", "salary": (10000, "$10,000"), "full_time": True},
                {"name": "Jim", "salary": (800, "$800"), "full_time": False},
                {"name": "Alice", "salary": (12500, "$12,500"), "full_time": True},
                {"name": "Bob", "salary": (7000, "$7,000"), "full_time": True}]

        # Loading it into gviz_api.DataTable
        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)

        # Create a JavaScript code string.
        jscode = data_table.ToJSCode("jscode_data",
                                     columns_order=("name", "salary", "full_time"),
                                     order_by="salary")
        # Create a JSON string.
        json = data_table.ToJSon(columns_order=("name", "salary", "full_time"),
                                 order_by="salary")
        data = {}
        data['cols'] = {}
        data['cols']['id'] = ''
        data['cols']['label'] = 'Titulo'
        data['cols']['pattern'] = ''
        data['cols']['type'] = 'string'
        # data['rows'] = {}
        # data['rows']['c'] = {}
        # data['rows']['c'] = "otrort"

        # data['chart'] = {}
        # data['chart']['type'] = ctype
        # data['xAxis'] = {}
        # data['xAxis']['categories'] = category_list
        # data['yAxis'] = {}
        # data['yAxis']['title'] = {"text": u'Seconds'}
        # data['series'] = series
        # data['legend'] = {}
        # data['legend']['layout'] = 'vertical'
        # data['legend']['align'] = 'right'
        # data['legend']['floating'] = True
        # data['legend']['verticalAlign'] = 'middle'

        return Response(data)
