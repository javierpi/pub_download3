"""
WSGI config for publications project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application
sys.path.append('/home/deployer/sites/pub_downloads3/pub_downloads/publications')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/deployer/sites/pub_downloads3/lib/python3.4/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'publications.settings'

# settings.configure()
application = get_wsgi_application()
