from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    blood_type = models.CharField(max_length=10, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emergency_contacts")
    
    # Adding blank=True and null=True fixes the terminal prompt error completely
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name or 'Unnamed Contact'} ({self.relationship or 'No Relation'})"

