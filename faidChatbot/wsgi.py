import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling # 👈 Implements Vercel file routing handlers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faidChatbot.settings')

# Wrap the application so it serves static assets and media photo directories cleanly
application = Cling(MediaCling(get_wsgi_application()))

# Global gateway hook used directly by Vercel deployment containers
app = application
