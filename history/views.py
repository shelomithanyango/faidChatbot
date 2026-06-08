from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import ChatHistory
from profiles.models import Profile

@login_required
def history_view(request):
    # Fetch or create the logged-in user's profile record
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Force Django to re-read the live database row
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

@login_required 
def export_chat_pdf(request):
    chats = ChatHistory.objects.filter(user=request.user)

    html_string = render_to_string("chat_pdf.html", {
        "chats": chats
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="chat.pdf"'
    
    # Generate the PDF file directly into the response stream
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    
    if pisa_status.err:
        return HttpResponse('We encountered some errors rendering your PDF.')
        
    return response
