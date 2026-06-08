from django.urls import path
from .views import profile_view, update_profile

app_name = 'profiles'

urlpatterns = [
    path("", profile_view, name="profile"),
     path("update/", update_profile, name="update_profile"),
    
]