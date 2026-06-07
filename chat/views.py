from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import get_chatbot_response
from history.models import ChatHistory


@login_required
def chat(request):
    user_name = request.user.first_name or request.user.username

    # Default welcome message
    reply = f"Hello {user_name}, how can I assist you today?"
    user_message = None

    if request.method == "POST":
        user_message = request.POST.get("message")

        if user_message:
            try:
                reply = get_chatbot_response(user_message)
                print("ABOUT TO SAVE CHAT")

                # Save conversation to history
                ChatHistory.objects.create(
                    user=request.user,
                    question=user_message,
                    response=reply
                )
                print("CHAT SAVED")

            except Exception:
                reply = "Sorry, something went wrong. Please try again later."

    return render(
        request,
        "chat/chat.html",
        {
            "reply": reply,
            "user_message": user_message,
            "user_name": user_name,
        }
    )