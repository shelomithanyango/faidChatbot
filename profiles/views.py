from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from history.models import ChatHistory
from .models import Profile

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    chats = ChatHistory.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    contacts = request.user.emergency_contacts.all()

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "contacts": contacts,
            "chats": chats
        }
    )