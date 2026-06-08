from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ChatHistory
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
# 1. IMPORT YOUR PROFILE MODEL FROM YOUR PROFILES APP
from profiles.models import Profile

@login_required
def history_view(request):
    # Fetch or create the logged-in user's profile record
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # FORCE DJANGO TO RE-READ THE LIVE DB ROW (Fixes cached image updates)
    profile.refresh_from_db()

    chats = ChatHistory.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'history/history.html',
        {
            'chats': chats,
            'profile': profile  
        }
    )


@login_required # Added login required decorator for safety
def export_chat_pdf(request):
    chats = ChatHistory.objects.filter(user=request.user)

    html_string = render_to_string("chat_pdf.html", {
        "chats": chats
    })

    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="chat.pdf"'
    return response
