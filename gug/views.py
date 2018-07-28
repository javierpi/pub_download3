# from apiclient.discovery import build
# from google.oauth2 import service_account
from gug.models import Google_service, Period, Publication, Stats, Dspace
from gug.forms import ApplicationForm
# import json
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Count, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
# from django.http import QueryDict
# from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


class index(ListView):
    context_object_name = 'periods'
    template_name = 'gug/index.html'

    def get_queryset(self):
        return Period.objects.annotate(Count('stats'))

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        return context


def stat_index_view(request):
    if request.method == "GET":
        form = ApplicationForm(request.GET)
        # if form.is_valid():
            # post = form.save(commit=False)
            # post.save()
        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)
        detail = request.GET.get('detail', 'off')
        gsid = request.GET.getlist('gsid', 1)
        period = request.GET.getlist('period', 1)

        if detail == 'on':
            print('Report: Detailed')
            stat_list = Stats.objects.select_related('id_dspace').\
                values('id_dspace__id_dspace', 'id_dspace__title', 'publication__tfile').\
                annotate(cuantity=Sum('cuantity')).\
                filter(google_service__in=gsid, period__in=period).\
                order_by('-cuantity')
        else:
            stat_list = Stats.objects.select_related('id_dspace').\
                values('id_dspace__id_dspace', 'id_dspace__title').\
                annotate(cuantity=Sum('cuantity')).\
                filter(google_service__in=gsid, period__in=period).\
                order_by('-cuantity')

        # print(request)
        period = Period.objects.filter(pk__in=period)
        gs = Google_service.objects.filter(pk__in=gsid)
        resume = Stats.objects.values('google_service').filter(google_service__in=gs, period__in=period).aggregate(totalrecords=Count('cuantity'), totalcuantity=Sum('cuantity'))
        paginator = Paginator(stat_list, pagesize)
        try:
            stats = paginator.page(page)
        except PageNotAnInteger:
            stats = paginator.page(1)
        except EmptyPage:
            stats = paginator.page(paginator.num_pages)

        return render(request, 'gug/stat.html', {'form': form, 'stats': stats, 'period': period, 'gs': gs, 'resume': resume, 'pagesize': pagesize, 'detail': detail})


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

class Listperiods(APIView):
    """
    View to list all periods in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


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
        return context


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
