from django.urls import path
from .views import chat_with_gemini, chatbot_home

urlpatterns = [
    path('', chatbot_home, name='chatbot_home'),
    path('chat/', chat_with_gemini, name='chat_with_gemini')
]
