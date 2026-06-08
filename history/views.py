from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import ChatHistory
from profiles.models import Profile

# ReportLab Imports for pure-Python PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

@login_required
def history_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.refresh_from_db()
    chats = ChatHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history/history.html', {'chats': chats, 'profile': profile})

@login_required 
def export_chat_pdf(request):
    # Set up the HTTP Response for a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="chat_history.pdf"'

    # Initialize the PDF document
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    # Set up text styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=20
    )
    message_style = ParagraphStyle(
        'MessageStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=12
    )

    # Document Header
    story.append(Paragraph("Chat History Export", title_style))
    story.append(Spacer(1, 10))

    # Pull user chats from the database
    chats = ChatHistory.objects.filter(user=request.user).order_by('created_at')

    if not chats.exists():
        story.append(Paragraph("No logs found for this account.", message_style))
    else:
        for chat in chats:
            # Format the output block text cleanly
            user_text = f"<b>You:</b> {chat.user_message}" if hasattr(chat, 'user_message') else f"<b>You:</b> {chat.message}"
            bot_text = f"<b>Bot:</b> {chat.bot_response}" if hasattr(chat, 'bot_response') else f"<b>Bot:</b> {chat.response}"
            
            story.append(Paragraph(user_text, message_style))
            story.append(Paragraph(bot_text, message_style))
            story.append(Spacer(1, 8)) # Space between messages

    # Render the elements cleanly into the document
    doc.build(story)
    return response
