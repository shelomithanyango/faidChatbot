from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import get_chatbot_response

@login_required
def chat(request):
    reply = None
    user_message = None

    # get the logged-in user's name
    user_name = request.user.first_name or request.user.username

    # default welcome message
    reply = f" Hello {user_name}, how can I assist you today?"

    if request.method == "POST":
        user_message = request.POST.get("message")

        if user_message:
            try:
                reply = get_chatbot_response(user_message)
            except Exception:
                reply = "Sorry, something went wrong. Please try again later."

    return render(request, "chat/chat.html", {
        "reply": reply,
        "user_message": user_message,
        "user_name": user_name
    })