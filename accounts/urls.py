from django.urls import path
from .views import profile_view

app_name = 'profile_view'
urlpatterns = [
    path("", profile_view, name="profile"),  
    
]