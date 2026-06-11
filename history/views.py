from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import ChatHistory
from profiles.models import Profile



@login_required
def history_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.refresh_from_db()
    chats = ChatHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history/history.html', {'chats': chats, 'profile': profile})

