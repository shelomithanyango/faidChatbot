import json
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from history.models import ChatHistory
from profiles.models import Profile 
from .services import get_chatbot_stream

@login_required
def chat(request):
    """Render the main chat page interface shell"""
    user_name = request.user.first_name or request.user.username
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    return render(
        request,
        "chat/chat.html",
        {
            "user_name": user_name,
            "profile": profile,  
        }
    )

@login_required
def chat_response_stream(request):
    """Asynchronous endpoint that handles simultaneous text token streaming"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if not user_message:
            return JsonResponse({"error": "No message provided"}, status=400)

        def event_generator():
            full_reply = ""
            # Stream each word chunk from Gemini immediately to the client
            for token in get_chatbot_stream(user_message):
                full_reply += token
                # Format chunk using Server-Sent Events (SSE) standard
                yield f"data: {json.dumps({'text': token})}\n\n"
            
            # Save transaction records to database after stream consumption completes
            ChatHistory.objects.create(
                user=request.user,
                question=user_message,
                response=full_reply
            )

        response = StreamingHttpResponse(event_generator(), content_type="text/event-stream")
        # Ensure Vercel / Nginx doesn't buffer or cache our stream data chunks
        response['X-Accel-Buffering'] = 'no'
        response['Cache-Control'] = 'no-cache'
        return response

    return JsonResponse({"error": "Method not allowed"}, status=405)
