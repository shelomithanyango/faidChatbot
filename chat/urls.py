from django.urls import path
from . import views
from .views import chat, chat_response_stream

app_name = 'chat'
urlpatterns = [
    path("", chat, name="chat"),  # /chat/ is now the chatbot
    path('stream/', views.chat_response_stream, name='chat_response_stream'),

    
]