"""
WSGI config for kiosk_app project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiosk_app.settings')

application = get_wsgi_application()

# Vercel utilise cette variable app
app = application 