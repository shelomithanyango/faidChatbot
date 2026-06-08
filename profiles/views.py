from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from history.models import ChatHistory
from .models import Profile, EmergencyContact

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    chats = ChatHistory.objects.filter(user=request.user).order_by('-created_at')[:5]
    contacts = request.user.emergency_contacts.all()

    return render(
        request,
        "profiles/profile.html",
        {
            "profile": profile,
            "contacts": contacts,
            "chats": chats
        }
    )

@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        #To update the important profile information    
        profile.age = request.POST.get("age") if request.POST.get("age") else None
        profile.blood_type = request.POST.get("blood_type")
        profile.allergies = request.POST.get("allergies")

        #for profile picture update
        if request.FILES.get("profile_pic"):
            profile.profile_pic = request.FILES["profile_pic"]
            
        profile.save()

        
        contact_ids = request.POST.getlist('contact_id[]')
        contact_names = request.POST.getlist('contact_name[]')
        contact_relationships = request.POST.getlist('contact_relationship[]')
        contact_phones = request.POST.getlist('contact_phone[]')

        for i in range(len(contact_ids)):
            try:
                contact = EmergencyContact.objects.get(id=contact_ids[i], user=request.user)
                contact.name = contact_names[i]
                contact.relationship = contact_relationships[i]
                contact.phone = contact_phones[i]
                contact.save()
            except EmergencyContact.DoesNotExist:
                pass

    return redirect("profiles:profile")
