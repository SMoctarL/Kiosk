"""
WSGI config for kiosk_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiosk_project.settings')

application = get_wsgi_application() 