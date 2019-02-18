# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from gug.models import Dspace

import subprocess
from bs4 import BeautifulSoup
import urllib.request as urllib2
import urllib.error
import ssl

class Command(BaseCommand):
      help = 'Get publications title from repositorio.cepal.org when they are blanks'
    
      # def add_arguments(self, parser):
      #       parser.add_argument('dspace_id', nargs='+', type=int)

      def handle(self, *args, **options):
            # id_dspace = models.PositiveIntegerField(default=0, help_text="ID Dspace", unique=True)
            # title = models.CharField(max_length=600, default='')
            # post_title1 = models.CharField(max_length=300, default='')
            # post_title2 = models.CharField(max_length=200, default='')
            context = ssl._create_unverified_context()
            dspace_titles = Dspace.objects.filter(title__exact='').order_by('id_dspace')
            for dspace_title in dspace_titles:
                  try:
                        
                        proto = 'https://'
                        subdo = 'repositorio.cepal.org'
                        urls = '/handle/11362/'
                        id_dspace = dspace_title.id_dspace
                        site = proto + str(subdo) + str(urls)  + str(dspace_title.id_dspace)
                        print(site)
                        try: 
                            URLObject = urllib2.urlopen(site, context=context)
                        except urllib2.HTTPError as e:
                            # checksLogger.error('HTTPError = ' + str(e.code))
                            print('HTTPError = ' + str(e.code))
                        except urllib2.URLError as e:
                            #checksLogger.error('URLError = ' + str(e.reason))
                            print('URLError = ' + str(e.reason))
                        except httplib.HTTPException as e:
                            #checksLogger.error('HTTPException')
                            print('HTTPException')
                        except Exception:
                            import traceback
                            #checksLogger.error('generic exception: ' + traceback.format_exc())
                            print('generic exception: ' + traceback.format_exc())

                        # try:
                        #       URLObject = urllib2.urlopen(site)
                        # except:
                        #       print('Some error')

                        else:
                              html = BeautifulSoup(URLObject.read(), features="html.parser")
                              title = html.find('title')
                              print(title.contents[0])
                              title = title.contents[0]
                              title = title[:599]
                              post_title1 = ''
                              post_title2 = ''
                              if title.count('|') == 2:
                                    post_title1 = title.split('|')[1]
                              if title.count('|') == 3:
                                    post_title2 = title.split('|')[2]
                              title = title.split('|')[0]
                              try:
                                    dsp = Dspace.objects.get(id_dspace=id_dspace)
                                    dsp.title=title
                                    dsp.post_title1=post_title1
                                    dsp.post_title2=post_title2
                                    dsp.save()
                              except dsp.DoesNotExist:
                                    print('Noexiste ??')
                        finally:
                              pass
                        
                        


                             

                  finally:
                        print("fin")
