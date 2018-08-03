from __future__ import unicode_literals
from __future__ import absolute_import
import sys
import csv

from gug.models import Google_service, Period, Publication, Stats, Dspace
from gug.forms import StatForm, DspaceForm
from gug.serializers import PeriodSerializer, StatsSerializer, DspaceSerializer

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Count, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse
from rest_framework import generics

from django.core.management import call_command
from django.core import management
from .management.commands import get_title


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def some_view(request):
	# values('id_dspace__id_dspace', 'id_dspace__title', 'publication__tfile').\
 #    annotate(cuantity=Sum('cuantity')).\
    gsid = request.GET.getlist('gsid', [1,])
    period = request.GET.getlist('period', [1,])
    stat_list = Stats.objects.select_related('id_dspace').\
        values('id_dspace__title', 'publication__tfile').\
        filter(google_service__in=gsid, period__in=period).\
        order_by('-cuantity')

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    row = ""
    rows = (["Row {}".format(idx), str(idx)] for idx in stat_list.all())
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    # for header in stat_list.all()[1]:
    # 	print(header)
    # 	row += header + ","
    # 	# for field in header:
    # 	# 	print(header[field])
    # writer.writerow(row)

#     for record in stat_list.all():
#         row = ""
#         for field in record:
# #        	print(record[field])
#             row += record[field] + ","
#         writer.writerow(row)
    

    return response
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    # rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    # pseudo_buffer = Echo()
    # writer = csv.writer(pseudo_buffer)
    # response = StreamingHttpResponse((writer.writerow(row) for row in rows),
    #                                  content_type="text/csv")
    # response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    # return response

def dspace_detail(request):
    if request.method == "GET":
        form = DspaceForm(request.GET)
        gsid = request.GET.getlist('gsid', 1)
        id_dspace = request.GET.get('id_dspace', 1)
        dspace_record = Dspace.objects.get(id_dspace=id_dspace)
        detail = request.GET.get('detail', 'off')
        if detail == 'on':
            stat_list = Stats.objects.select_related('id_dspace', 'period').\
                values('id_dspace__id_dspace', 'period__start_date', 'publication__tfile').\
                annotate(cuantity=Sum('cuantity')).\
                filter(id_dspace__id_dspace=id_dspace, google_service__in=gsid).\
                order_by('period__start_date')
        else:
            stat_list = Stats.objects.select_related('id_dspace', 'period').\
                values('id_dspace__id_dspace', 'period__start_date').\
                annotate(cuantity=Sum('cuantity')).\
                filter(id_dspace__id_dspace=id_dspace, google_service__in=gsid).\
                order_by('period__start_date')


        gs = Google_service.objects.filter(pk__in=gsid)

        return render(request, 'gug/dspace_detail.html', {'form': form, 'stats': stat_list, 'gs': gs, 'dspace_record': dspace_record, 'detail': detail})


class index(ListView):
    context_object_name = 'periods'
    template_name = 'gug/index.html'

    def get_queryset(self):
        return Period.objects.annotate(Count('stats'))

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        return context



@api_view(['GET'])
def stat_index_view(request):
    if request.method == "GET":
        form = StatForm(request.GET)
        # if form.is_valid():
        # post = form.save(commit=False)
        # post.save()
        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)
        detail = request.GET.get('detail', 'off')
        json = request.GET.get('json', 'off')
        gsid = request.GET.getlist('gsid', 1)
        period = request.GET.getlist('period', 1)

        if detail == 'on':
            print('Report: Detailed')
            if json == 'on':
            	stat_list = Stats.objects.select_related('id_dspace').\
                    filter(google_service__in=gsid, period__in=period).\
                    order_by('-cuantity')
            else:
                stat_list = Stats.objects.select_related('id_dspace').\
                    values('id_dspace__id_dspace', 'id_dspace__title', 'publication__tfile').\
                    annotate(cuantity=Sum('cuantity')).\
                    filter(google_service__in=gsid, period__in=period).\
                    order_by('-cuantity')
        else:
            stat_list = Stats.objects.select_related('id_dspace').\
                values('id_dspace__id', 'id_dspace__id_dspace', 'id_dspace__title').\
                annotate(cuantity=Sum('cuantity')).\
                filter(google_service__in=gsid, period__in=period).\
                order_by('-cuantity')

        # print(request)
        

        
        if json == 'on':
            serializer = StatsSerializer(stat_list, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            period = Period.objects.filter(pk__in=period)
            gs = Google_service.objects.values_list('id', flat=True).filter(pk__in=gsid)
            resume = Stats.objects.values('google_service').filter(google_service__in=gs, period__in=period).aggregate(totalrecords=Count('cuantity'), totalcuantity=Sum('cuantity'))

            paginator = Paginator(stat_list, pagesize)
            try:
                stats = paginator.page(page)
            except PageNotAnInteger:
                stats = paginator.page(1)
            except EmptyPage:
                stats = paginator.page(paginator.num_pages)
            return render(request, 'gug/stat.html', {'form': form, 'stats': stats, 'period': period, 'gs': gsid, 'resume': resume, 'pagesize': pagesize, 'detail': detail})


class periods_detail(DetailView):
    model = Period
    template_name = 'gug/periods_detail.html'

    def get_context_data(self, **kwargs):
        context = super(periods_detail, self).get_context_data(**kwargs)
        context['google_service'] = Google_service.objects.all()
        context['statistics'] = Stats.objects.values('google_service').filter(period=self.get_object()).annotate(Count('cuantity'), Sum('cuantity')).order_by()
        context['resume'] = Stats.objects.values('google_service').filter(period=self.get_object()).aggregate(totalrecords=Count('cuantity'), totalcuantity=Sum('cuantity'))
        return context


class periods(ListView):
    context_object_name = 'periods'
    template_name = 'gug/periods.html'

    def get_queryset(self):
        return Period.objects.annotate(Count('stats')).annotate(cuantity=Sum('stats__cuantity'))

    def get_context_data(self, **kwargs):
        context = super(periods, self).get_context_data(**kwargs)
        return context



#class api_stat(generics.ListAPIView):
@api_view(['GET'])
def api_stat(request):
    if request.method == 'GET':
        # stat_list = Stats.objects.all()
        detail = request.GET.get('detail', 'off')
        gsid = request.GET.getlist('gsid', 1)
        period = request.GET.getlist('period', 1)
        id_dspace = request.GET.getlist('id_dspace', None)
        stat_list = Stats.objects.select_related('id_dspace', 'google_service').\
            values('id_dspace__id_dspace', 'id_dspace__title', 'publication__tfile').\
            annotate(cuantity=Sum('cuantity')).\
            filter(google_service__in=gsid, period__in=period).\
            order_by('-cuantity')

    # if id_dspace is not None:
    #     stat_list = stat_list.filter(id_dspace=id_dspace)

        serializer = StatsSerializer(stat_list, many=True)
        return Response(serializer.data)

# @api_view(['GET'])
# def api_stat(request):
#     if request.method == 'GET':
#         detail = request.GET.get('detail', 'off')
#         gsid = request.GET.getlist('gsid', (1,2))
#         period = request.GET.getlist('period', (1,2))

#         # if detail == 'on':
# #        print('Report: Detailed')
#         stat_list = Stats.objects.select_related('id_dspace', 'google_service').\
#             values('id_dspace__id_dspace', 'id_dspace__title', 'publication__tfile').\
#             annotate(cuantity=Sum('cuantity')).\
#             filter(google_service__in=gsid, period__in=period).\
#             order_by('-cuantity')
#         # else:
#         #     stat_list = Stats.objects.select_related('id_dspace').\
#         #         values('id_dspace__id', 'id_dspace__id_dspace', 'id_dspace__title').\
#         #         annotate(cuantity=Sum('cuantity')).\
#         #         filter(google_service__in=gsid, period__in=period).\
#         #         order_by('-cuantity')
#         serializer = StatsSerializer(stat_list, many=True)
#         return  Response(serializer.data)

        

@api_view(['GET'])
def api_publication_detail(request, pk):
    try:
        publication = Publication.objects.get(pk=pk)
    except publication.DoesNotExist:
        return HttpResponse(status=404)
  
    if request.method == 'GET':
        serializer = PublicationSerializer(publication, many=True)
        return  Response(serializer.data)

@api_view(['GET'])
def api_periods_list(request):
  
    if request.method == 'GET':
        periods = Period.objects.all()
        serializer = PeriodSerializer(periods, many=True)
        return  Response(serializer.data)

@api_view(['GET'])
def api_periods_detail(request, pk):
    try:
        periods = Period.objects.get(pk=pk)
    except periods.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PeriodSerializer(periods)
        return Response(serializer.data)

    

class google_services_detail(DetailView):
    model = Google_service
    template_name = 'gug/google_service_detail.html'

    def get_context_data(self, **kwargs):
        context = super(google_services_detail, self).get_context_data(**kwargs)
        context['periods'] = Period.objects.all()
        context['statistics'] = Stats.objects.values('period').filter(google_service=self.get_object()).annotate(Count('cuantity'), Sum('cuantity')).order_by()
        context['resume'] = Stats.objects.values('google_service').filter(google_service=self.get_object()).aggregate(totalrecords=Count('cuantity'), totalcuantity=Sum('cuantity'))
        return context


class google_services(ListView):
    context_object_name = 'google_service'
    template_name = 'gug/google_service.html'

    def get_queryset(self):
        return Google_service.objects.annotate(Count('stats')).annotate(cuantity=Sum('stats__cuantity'))

    def get_context_data(self, **kwargs):
        context = super(google_services, self).get_context_data(**kwargs)
        return context

def get_title(request, dspace_id):
    print(int(dspace_id))
    try:
    	#management.call_command('get_title', dspace_id=int(dspace_id), verbosity=2, interactive=False)
    	management.call_command('get_title', verbosity=2)
    except:
    	print("Unexpected error:", sys.exc_info()[0])
    	raise

    	

    return redirect('/dspace/?id_dspace=' + dspace_id + '&gsid=3')

# def get_GCS(request):
#     SCOPE_WEBMASTER = 'https://www.googleapis.com/auth/webmasters.readonly'
#     CLIENT_SECRETS_PATH = 'DownloadPublicaciones-a610ebc17b1e.json'
#     REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
#     property_uri = 'http://repositorio.cepal.org'
#     credentials = service_account.Credentials.from_service_account_file(CLIENT_SECRETS_PATH, scopes=SCOPE_WEBMASTER)
#     if credentials is None:
#         print("BAD CREDENTIALS")

#     #authed_http = AuthorizedHttp(credentials)
#     service = build('webmasters', 'v3')
#     output_rows = []
#     request = {
#         "startDate": "2018-06-01",
#         "endDate": "2018-06-30",
#         "dimensions": ["page"],
#         "searchType": "web",
#         "rowLimit": 20000,
#         "startRow": 0,
#         "aggregationType": "byPage",
#         "fileType": "pdf",
#         "dimensionFilterGroups": [
#             {
#                 "filters": [{
#                     "dimension": "page",
#                     "expression": "bitstream",
#                     "operator": "contains"
#                 },
#                     {
#                     "dimension": "page",
#                     "expression": "pdf",
#                     "operator": "contains"
#                 },
#                     {
#                     "dimension": "page",
#                     "expression": ".txt",
#                     "operator": "notcontains"
#                 }
#                 ]
#             }
#         ]
#     }
#     response = service.searchanalytics().query(siteUrl=property_uri, body=request).execute()
#     if 'rows' in response:
#         row_count = 0
#         for row in response['rows']:
#             row_count = row_count + 1
#             keys = ','.join(row['keys'])
#             #output_row = [keys, row['clicks'], row['impressions'], row['ctr'], row['position']]
#             output_row = [keys, row['clicks']]
#             print(row_count, output_row)

    # print(response)
