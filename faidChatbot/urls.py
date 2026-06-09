"""
URL configuration for faidChatbot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from django.http import HttpResponse
from django.core.management import call_command
import os


def run_prod_migrations(request):
    # Only allow this to run on Vercel to protect your database
    if os.environ.get('VERCEL') == '1':
        try:
            call_command('migrate', interactive=False)
            return HttpResponse("Database Migrations Successfully Completed!")
        except Exception as e:
            return HttpResponse(f"Migration Failed: {e}", status=500)
    return HttpResponse("Not Allowed", status=403)

urlpatterns = [
    path('',include('homepage.urls')),
    path('run-secret-migrations/', run_prod_migrations),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path("chat/", include("chat.urls")),
    path('', include('authentication.urls')),
    path('ussd/', include('ussd.urls')),
    path('profiles/', include('profiles.urls')),
    path('history/', include('history.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)