from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ChatHistory

@login_required
def history_view(request):
    chats = ChatHistory.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'history/history.html',
        {'chats': chats}
    )