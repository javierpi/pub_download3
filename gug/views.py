from __future__ import unicode_literals
from __future__ import absolute_import
import sys
import csv
import gviz_api
# import unicodecsv as csv
import codecs
import json

#### 
####

from gug.models import Google_service, Period, Publication, Stats, Dspace, Service_group
from gug.forms import StatForm, DspaceForm, IndexForm
from gug.serializers import PeriodSerializer, StatsSerializer, StatsSerializer3
from gug.tasks import get_GA

from django import forms
from django.forms import formset_factory
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Count, Sum
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse
from rest_framework import generics, serializers, viewsets, views
from rest_framework.renderers import JSONRenderer


from django.core import management
from .management.commands import get_title
from .serializers import StatsSerializer


@cache_page(60 * 15)
@csrf_exempt
def stat_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        stats = Period.objects.all()
        serializer = StatsSerializer(stats, many=True)
        return JsonResponse(serializer.data, safe=False)


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def dspace_detail_tmp(request):
    if request.method == "GET":
        id_dspace = request.GET.get('id_dspace', 1)
        
        gsid_avalable = list(Google_service.objects.values_list('id', flat=True).order_by('pk'))
        period_avalable = list(Period.objects.values_list('id', flat=True))

        per_list = ""
        for x in period_avalable:
            per_list += '&period='+str(x)

        gs_list = ""
        for x in gsid_avalable:
            gs_list += '&gsid=' + str(x)

        period = per_list
        gsid = gs_list
        print("/dspace/?id_dspace=" +id_dspace +  gsid + period)
        return redirect("/dspace/?id_dspace=" +id_dspace +  gsid + period)


# @cache_page(60 * 15)
def dspace_detail(request):
    if request.method == "GET":
        form = DspaceForm(request.GET)
        
        gsid_avalable = list(Google_service.objects.values_list('id', flat=True))
        gs_list = []
        for x in gsid_avalable:
            gs_list.append(str(x))
        gsid = request.GET.getlist('gsid', gs_list)
        gstitles = Google_service.objects.filter(pk__in=gsid)
        gs = Google_service.objects.values_list('id', flat=True).filter(pk__in=gsid)

        period_avalable = list(Period.objects.values_list('id', flat=True))
        per_list = []
        for x in period_avalable:
            per_list.append(str(x))
        period = request.GET.getlist('period', per_list)

        id_dspace = request.GET.get('id_dspace', 1)

        fields = ['Period']
        for title in gstitles:
            fields.append(title.name.split(' '))
        fields.append('Total Downloads')
        table = {'headers': fields}

        query_resume_inicial = "select  'Total' as tit1, "
        query_resume_rows = ""
        query_resume_final = ", sum(cuantity) as sumtotal " \
                            " from gug_stats as gs_master " \
                            " inner join gug_dspace on gs_master.id_dspace_id = gug_dspace.id "\
                            " where gs_master.google_service_id in (" + ','.join(gsid) + ")" \
                            " and id_dspace = " + id_dspace + " " 
        query_resume_final += " and period_id in (" + ','.join(period) + ") "

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
                            " and id_dspace = " + id_dspace + " " 
        group_query_resume_final += " and period_id in (" + ','.join(period) + ") "
        #

        group_query_inicial = "select gug_period.start_date , "
        group_query_rows = ""
        group_query_final = ", sum(cuantity) as sumtotal from gug_stats as gs_master " \
                    " inner join gug_dspace on gs_master.id_dspace_id = gug_dspace.id "\
                    " inner join gug_period on gs_master.period_id = gug_period.id  " \
                    " inner join gug_google_service on gs_master.google_service_id = gug_google_service.id " \
                    " where gs_master.google_service_id in (" + ','.join(gsid) + ") " \
                    " and period_id in (" + ','.join(period) + ") " \
                    " and id_dspace = " + id_dspace + " " \
                    " group by gs_master.period_id order by gug_period.start_date desc "
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
            group_query_resume_rows += "(select sum(cuantity) as " + sumvar + " " \
                                " from gug_stats as " + fromvar + " " \
                                " inner join gug_dspace on " + fromvar + ".id_dspace_id = gug_dspace.id "\
                                " where google_service_id in (" + ','.join(groupids2) + ") " \
                                " and id_dspace = " + id_dspace + " " \
                                " and period_id in (" + ','.join(period) + ")  ) AS '" + sumvar + "' ,"
            group_query_rows += "(select sum(cuantity)  as " + sumvar + " " \
                        " from gug_stats as " + fromvar + "" \
                        " inner join gug_dspace on " + fromvar + ".id_dspace_id = gug_dspace.id  " \
                        " where google_service_id in (" + ','.join(groupids2) + ") " \
                        " and period_id =  gs_master.period_id " \
                        " and id_dspace = " + id_dspace + " " \
                        " ) AS '" + sumvar + "' ,"

            ## Group detail
            query_grp_inicial = "select gug_period.start_date , "
            query_grp_final = ", sum(cuantity) as sumtotal from gug_stats as gs_master " \
                    " inner join gug_dspace on gs_master.id_dspace_id = gug_dspace.id "\
                    " inner join gug_period on gs_master.period_id = gug_period.id  " \
                    " where gs_master.google_service_id in (" + ','.join(groupids2) + ") " \
                    " and period_id in (" + ','.join(period) + ") " \
                    " and id_dspace = " + id_dspace + " " \
                    " group by gs_master.period_id order by gug_period.start_date desc "
            query_grp_serv = ''

            query_grp_resume_inicial = "select  'Total' as tit1, "
            query_grp_resume_rows = ""
            query_grp_resume_final = ", sum(cuantity) as sumtotal " \
                                " from gug_stats as gs_master " \
                                " inner join gug_dspace on gs_master.id_dspace_id = gug_dspace.id "\
                                " inner join gug_google_service on gs_master.google_service_id = gug_google_service.id " \
                                " where gs_master.google_service_id in (" + ','.join(groupids2) + ") " \
                                " and period_id in (" + ','.join(period) + ") " \
                                " and id_dspace = " + id_dspace + " " 
            for gsA in groupids2:
                query_grp_serv += "(select sum(cuantity)  " \
                        " from gug_stats " \
                        " inner join gug_dspace on gug_stats.id_dspace_id = gug_dspace.id  " \
                        " where google_service_id = " + str(gsA) + " " \
                        " and id_dspace = " + id_dspace + " " \
                        " and period_id =  gs_master.period_id " \
                        " ) AS '" + sumvar + "' ,"
                query_grp_resume_rows += "(select sum(cuantity) as " + sumvar + " " \
                                    " from gug_stats as gs1 " \
                                    " inner join gug_dspace on gs1.id_dspace_id = gug_dspace.id "\
                                    " where google_service_id = " + str(gsA) + " " \
                                    " and id_dspace = " + id_dspace + " " \
                                    " and period_id in (" + ','.join(period) + ")  ) AS '" + sumvar + "' ,"

            query_grp = query_grp_inicial + query_grp_serv[:-1] + query_grp_final
            grp_resume = query_grp_resume_inicial + query_grp_resume_rows[:-1] + query_grp_resume_final
            cursor = connection.cursor()
            cursor.execute(query_grp)
            group_list = cursor.fetchall()
            ## para resume
            # cursor = connection.cursor()
            cursor.execute(grp_resume)
            resume_list = cursor.fetchall()

            group_name = Service_group.objects.get(pk=groupn).name
            google_services_groups.append({'name': group_name, 'values': group_list, 'headers': fields, 'resume': resume_list})

            
        group_sql = group_query_inicial + group_query_rows[:-1] + group_query_final 
        cursor = connection.cursor()
        cursor.execute(group_sql)
        group_list = cursor.fetchall()

        group_query_resume = group_query_resume_inicial + group_query_resume_rows[:-1] + group_query_resume_final
        cursor = connection.cursor()
        cursor.execute(group_query_resume)
        group_resume = cursor.fetchall()
        #### --

        # query_inicial = "select gug_period.start_date , "
        # query_rows = ""
        # query_final = ", sum(cuantity) as sumtotal from gug_stats as gs_master " \
        #             " inner join gug_dspace on gs_master.id_dspace_id = gug_dspace.id "\
        #             " inner join gug_period on gs_master.period_id = gug_period.id  " \
        #             " where gs_master.google_service_id in (" + ','.join(gsid) + ") " \
        #             " and period_id in (" + ','.join(period) + ") " \
        #             " and id_dspace = " + id_dspace + " " \
        #             " group by gs_master.period_id order by gug_period.start_date desc "

        # num_cols = 0
        # for gsn in gsid:
        #     num_cols += 1
        #     sumvar = "sumags" + str(num_cols)
        #     scolvar = "colags" + str(num_cols)
        #     query_resume_rows += "(select sum(cuantity) as " + sumvar + " " \
        #                         " from gug_stats as gs1 " \
        #                         " inner join gug_dspace on gs1.id_dspace_id = gug_dspace.id "\
        #                         " where google_service_id = " + str(gsn) + " " \
        #                         " and id_dspace = " + id_dspace + " " \
        #                         " and period_id in (" + ','.join(period) + ")  ) AS '" + sumvar + "' ,"
        #     query_rows += "(select sum(cuantity)  " \
        #                 " from gug_stats " \
        #                 " inner join gug_dspace on gug_stats.id_dspace_id = gug_dspace.id  " \
        #                 " where google_service_id = " + str(gsn) + " " \
        #                 " and id_dspace = " + id_dspace + " " \
        #                 " and period_id =  gs_master.period_id " \
        #                 " ) AS '" + sumvar + "' ,"


        period_objs = Period.objects.filter(pk__in=period)

        # query_resume = query_resume_inicial + query_resume_rows[:-1] + query_resume_final
        # cursor = connection.cursor()
        # cursor.execute(query_resume)
        # resume = cursor.fetchall()

        
        # final_sql = query_inicial + query_rows[:-1] + query_final 
        # # print('final_sql = ', final_sql)
        # cursor = connection.cursor()
        # cursor.execute(final_sql)
        # stat_list = cursor.fetchall()

        # table.update({'rows': stat_list})
        table.update({'groupheaders': fields2})
        table.update({'group_rows': group_list})
        table.update({'group_resume': group_resume})
        table.update({'group_statistics': google_services_groups})
        table.update({'period': period})
        # table.update({'resume': resume})
        dspace_record = Dspace.objects.get(id_dspace=id_dspace)
        return render(request, 'gug/dspace_detail.html', {'form': form, 'table': table,  'period': period_objs, 'gs': gs, 'dspace_record': dspace_record})
        # , 'resume': resume


@api_view(['GET'])
def dspace_detail1(request):

    if request.method == "GET":
        form = DspaceForm(request.GET)
        gsid = request.GET.getlist('gsid', 1)
        id_dspace = request.GET.get('id_dspace', 1)
        gs = Google_service.objects.filter(pk__in=gsid)
        detail = request.GET.get('detail', 'off')
        period = request.GET.getlist('period', 1)

        try:
            dspace_record = Dspace.objects.get(id_dspace=id_dspace)
            period_objs = Period.objects.filter(pk__in=period)
            if detail == 'on':
                # values('id_dspace__id_dspace', 'period__start_date', 'publication__tfile').\
                stat_list = Stats.objects.select_related('id_dspace', 'period').\
                    filter(id_dspace__id_dspace=id_dspace, google_service__in=gsid, period__in=period).\
                    values('period__start_date', 'publication__tfile').\
                    annotate(cuantity=Sum('cuantity')).\
                    order_by('-period__start_date')
            else:
                stat_list = Stats.objects.select_related('id_dspace', 'period').\
                    values('id_dspace__id_dspace', 'period__start_date').\
                    annotate(cuantity=Sum('cuantity')).\
                    filter(id_dspace__id_dspace=id_dspace, google_service__in=gsid, period__in=period).\
                    order_by('-period__start_date')

            resume = Stats.objects.values('google_service').filter(id_dspace__id_dspace=id_dspace, google_service__in=gsid, period__in=period).aggregate(totalrecords=Count('cuantity'), totalcuantity=Sum('cuantity'))
        except Dspace.DoesNotExist:
            stat_list = []
            dspace_record = {}
            dspace_record['id_dspace'] = 1
            dspace_record['title'] = 'Not Found'
            resume = []
            period_objs = []

        return render(request, 'gug/dspace_detail.html', {'form': form, 'stats': stat_list, 'gs': gs, 'dspace_record': dspace_record, 'detail': detail, 'resume': resume, 'period': period_objs})


def dspace_detail2(request):
    if request.method == "GET":
        form = DspaceForm(request.GET)
        gsid = request.GET.getlist('gsid', 1)
        id_dspace = request.GET.get('id_dspace', 1)
        dspace_record = Dspace.objects.get(id_dspace=id_dspace)
        detail = request.GET.get('detail', 'off')

        query_inicial = "select gp1.id, gug_period.start_date, gp1.tfile, "
        query_rows = ""
        query_final = ", sum(cuantity) as sumtotal from gug_stats as gs_master"\
            " inner join gug_dspace ON gs_master.id_dspace_id = gug_dspace.id " \
            " inner join gug_publication gp1 ON gug_dspace.id_dspace = gug_publication.id_dspace_id" \
            " inner join gug_period ON gs_master.period_id = gug_period.id " \
            " where gs_master.google_service_id in (" + ','.join(gsid) + ") and "\
            " gug_dspace.id_dspace = " + str(id_dspace) + ""\
            " group by gp1.id, period_id " \
            " order by gug_period.start_date asc "

        num_cols = 0
        for gsn in gsid:
            num_cols += 1
            sumvar = "sumags" + str(num_cols)
            query_rows += "(select sum(cuantity) from gug_stats as gs1 "\
                " inner join gug_dspace ON gs1.id_dspace_id = gug_dspace.id " \
                " inner join gug_publication ON gug_dspace.id_dspace = gug_publication.id_dspace_id" \
                " inner join gug_period ON gs1.period_id = gug_period.id " \
                " where google_service_id = " + str(gsn) + " and "\
                " gug_dspace.id_dspace = " + str(id_dspace) + " and "\
                " gug_publication.id = gp1.id " \
                " group by gug_publication.id, period_id  " \
                " order by gug_period.start_date asc) AS 'gs1' ,"

        final_sql = query_inicial + query_rows[:-1] + query_final  # todos
        query_resume = query_inicial + query_rows[8:-12]  # Solo internos

        print(final_sql)
        cursor = connection.cursor()
        cursor.execute(final_sql)
        stats = cursor.fetchall()

        cursor = connection.cursor()
        cursor.execute(query_resume)
        resume = cursor.fetchall()

        gs = Google_service.objects.filter(pk__in=gsid)
        gstitles = Google_service.objects.filter(pk__in=gsid)
        fields = ['ID Dspace', 'Period']
        if detail == 'on':
            fields.append('Filename')
        for title in gstitles:
            # fields.append(title.name[0:10])
            fields.append(title.name.split(' '))
        fields.append('Total Downloads')

        stat_list = {'headers': fields}
        stat_list.update({'rows': stats})
        stat_list.update({'resume': resume})

        # resume = Stats.objects.values('google_service').filter(id_dspace__id_dspace=id_dspace, google_service__in=gsid, period__in=period).aggregate(totalrecords=Count('cuantity'), totalcuantity=Sum('cuantity'))

        # return render(request, 'gug/dspace_detail.html', {'form': form, 'table': table,     'gs': gs, 'dspace_record': dspace_record, 'detail': detail})
        return render(request, 'gug/dspace_detail.html', {'form': form, 'stats': stat_list, 'gs': gs, 'dspace_record': dspace_record, 'detail': detail})
        return render(request, 'gug/dspace_detail.html', {'form': form, 'stats': stat_list, 'gs': gs, 'dspace_record': dspace_record, 'detail': detail, 'resume': resume, 'period': period_objs})


#@cache_page(60 * 15)
def index(request):
    context_object_name = 'periods'

    form = IndexForm()
      
    context = {}
    context['periods'] = Period.objects.annotate(cuantity=Sum('stats__cuantity')).order_by('-start_date')
    context['statistics'] = Stats.objects.values('google_service').annotate(Count('cuantity'), Sum('cuantity')).order_by()
    ###########
    grupos = Service_group.objects.all()
    google_services_groups = []
    for grupo in grupos:
        group_stat = Stats.objects.values('google_service').filter(google_service_id__group=grupo.id).aggregate(totalrecords=Count('cuantity'), totalcuantity=Sum('cuantity'))
        google_services_groups.append({'name': grupo.name, 'values': Google_service.objects.values('id', 'name', 'view_id').filter(group=grupo.id), 'resume': group_stat})

    context['group_statistics'] = google_services_groups
    context['resume'] = Stats.objects.values('google_service').aggregate(totalrecords=Count('cuantity'), totalcuantity=Sum('cuantity'))

    q_dspace = " select gug_dspace.id_dspace, gug_dspace.title , sum(cuantity) as sumtotal " \
            " from gug_stats as gs_master " \
            " inner join gug_dspace on gs_master.id_dspace_id = gug_dspace.id " \
            " group by id_dspace_id order by sumtotal desc limit 0,10;"

    cursor = connection.cursor()
    cursor.execute(q_dspace)
    context['dspaces'] = cursor.fetchall()

    return render(request, 'gug/index.html', {'form': form,  'table': context })
   

def iter_csv(rows, pseudo_buffer):
    yield pseudo_buffer.write(codecs.BOM_UTF8)
    writer = csv.writer(pseudo_buffer)
    for row in rows:
        yield writer.writerow(row)


@cache_page(60 * 15)
@api_view(['GET'])
def stat_index_view(request):
    if request.method == "GET":
        # ArticleFormSet = formset_factory(StatForm, extra=0)
        form = StatForm(request.GET)

        if form.is_valid():
            print('form valido')
        else:
            print('form NO valido !!!! ')
            form = StatForm(request.GET)

        #form.page = 2
        gsid_avalable = list(Google_service.objects.values_list('id', flat=True))

        period_avalable = list(Period.objects.values_list('id', flat=True))
        per_list = []
        for x in period_avalable:
            per_list.append(str(x))

        gs_list = []
        for x in gsid_avalable:
            gs_list.append(str(x))

        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)

        limits_start = (int(page) * int(pagesize)) - int(pagesize)
        limits_end = int(page) * int(pagesize)
        query_limits = ' limit ' + str(limits_start) + ', ' + str(limits_end)
        # detail = request.GET.get('detail', 'off')
        csv_output = request.GET.get('csv_output', 'off')

        gsid = request.GET.getlist('gsid', gs_list)
        period = request.GET.getlist('period', per_list)

        gs = Google_service.objects.values_list('id', flat=True).filter(pk__in=gsid)
        gstitles = Google_service.objects.filter(pk__in=gsid)

        fields = ['Dspace ID', 'Title']
        for title in gstitles:
            fields.append(title.name.split(' '))
        fields.append('Total Downloads')
        table = {'headers': fields}
        query_resume_inicial = "select  'Total' as tit1, count(*) as tit2, "
        query_resume_rows = ""
        query_resume_final = ", sum(cuantity) as sumtotal from gug_stats as gs_master where gs_master.google_service_id in (" + ','.join(gsid) + ")"
        query_resume_final += " and period_id in (" + ','.join(period) + ") "
        query_inicial = "select gug_dspace.id_dspace, gug_dspace.title , "
        query_rows = ""
        query_final = ", sum(cuantity) as sumtotal from gug_stats as gs_master inner join gug_dspace on gs_master.id_dspace_id = gug_dspace.id where gs_master.google_service_id in (" + ','.join(gsid) + ") and period_id in (" + ','.join(period) + ") group by id_dspace_id order by sumtotal desc "
        num_cols = 0
        for gsn in gsid:
            num_cols += 1
            sumvar = "sumags" + str(num_cols)
            query_resume_rows += "(select sum(cuantity) as " + sumvar + " from gug_stats as gs1 where google_service_id = " + str(gsn) + " and period_id in (" + ','.join(period) + ")  ) AS '" + sumvar + "' ,"
            query_rows += "(select sum(cuantity) as " + sumvar + " from gug_stats as gs1 where google_service_id = " + str(gsn) + " and period_id in (" + ','.join(period) + ") and gs_master.id_dspace_id = gs1.id_dspace_id group by id_dspace_id ) AS '" + sumvar + "' ,"

        query_resume = query_resume_inicial + query_resume_rows[:-1] + query_resume_final
        cursor = connection.cursor()
        cursor.execute(query_resume)
        resume = cursor.fetchall()

        period_objs = Period.objects.filter(pk__in=period)

        if csv_output == 'on':
            # No records limit for CSV
            final_sql = query_inicial + query_rows[:-1] + query_final
            print(final_sql)
            cursor = connection.cursor()
            cursor.execute(final_sql)
            stat_list = cursor.fetchall()
            rows = []
            row = []
            colcount = 0
            for head in fields:
                colcount += 1
                if colcount > 2:
                    row.append(' '.join(head))
                else:
                    row.append(head)
            rows.append(row)

            for record in stat_list:
                row = []
                for col in list(range(0, len(fields))):
                    if col == 1:
                        row.append('"' + str(record[col]) + '"')
                        # row.append(str(record[col]))
                    else:
                        row.append(record[col])
                rows.append(row)

            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer)
            response = StreamingHttpResponse(iter_csv(rows, Echo()), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="pub_downloads.csv"'

            return response

        else:
            final_sql = query_inicial + query_rows[:-1] + query_final + query_limits
            print(final_sql)
            cursor = connection.cursor()
            cursor.execute(final_sql)
            stat_list = cursor.fetchall()

            paginator = Paginator(stat_list, pagesize)
            try:
                stats = paginator.page(page)
            except PageNotAnInteger:
                stats = paginator.page(1)
            except EmptyPage:
                stats = paginator.page(paginator.num_pages)

            table.update({'rows': stats})
            table.update({'period': period})
            table.update({'resume': resume})
            return render(request, 'gug/stat.html', {'form': form, 'table': table, 'period': period_objs, 'gs': gsid, 'resume': resume, 'pagesize': pagesize})



def periods_detail(request, pk):
    context_object_name = 'periods'
    model = Period
    grupos = Service_group.objects.all()

    context = {}
    google_services_groups = []

    context['period'] = Period.objects.get(id=pk)
    context['google_service'] = Google_service.objects.all()
    context['statistics'] = Stats.objects.values('google_service').filter(period_id=pk).annotate(Count('cuantity'), Sum('cuantity')).order_by()
    for grupo in grupos:
        group_stat = Stats.objects.values('google_service').filter(google_service_id__group=grupo.id).filter(period_id=pk).aggregate(totalrecords=Count('cuantity'), totalcuantity=Sum('cuantity'))
        google_services_groups.append({'name': grupo.name, 'values': Google_service.objects.values('id', 'name', 'view_id').filter(group=grupo.id), 'resume': group_stat})

    context['group_statistics'] = google_services_groups
    context['resume'] = Stats.objects.values('google_service').filter(period_id=pk).aggregate(totalrecords=Count('cuantity'), totalcuantity=Sum('cuantity'))
    
    q_dspace = " select gug_dspace.id_dspace, gug_dspace.title , sum(cuantity) as sumtotal " \
            " from gug_stats as gs_master " \
            " inner join gug_dspace on gs_master.id_dspace_id = gug_dspace.id " \
            " where gs_master.period_id = " + pk + "" \
            " group by id_dspace_id order by sumtotal desc limit 0,20;" 

    cursor = connection.cursor()
    cursor.execute(q_dspace)
    context['dspaces'] = cursor.fetchall()

    return render(request, 'gug/periods_detail.html', {'table': context })


class periods(ListView):
    context_object_name = 'periods'
    template_name = 'gug/periods.html'

    def get_queryset(self):
        return Period.objects.annotate(Count('stats')).annotate(cuantity=Sum('stats__cuantity')).order_by('-start_date')

    def get_context_data(self, **kwargs):
        context = super(periods, self).get_context_data(**kwargs)
        return context


@cache_page(60 * 15)
@api_view(['GET'])
def api_publication_detail(request, pk):
    try:
        publication = Publication.objects.get(pk=pk)
    except publication.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PublicationSerializer(publication, many=True)
        return Response(serializer.data)


@cache_page(60 * 15)
@api_view(['GET'])
def api_periods_list(request):

    if request.method == 'GET':
        periods = Period.objects.all()
        serializer = PeriodSerializer(periods, many=True)
        return Response(serializer.data)


@cache_page(60 * 15)
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
        context['statistics'] = Stats.objects.values('period', 'period__start_date').filter(google_service=self.get_object()).annotate(Count('cuantity'), Sum('cuantity')).order_by('-period__start_date')
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



def get_titles(request):
    try:
        management.call_command('get_title', verbosity=2)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    return redirect('/')

def get_ga(request):
    try:
        get_GA()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    return redirect('/')