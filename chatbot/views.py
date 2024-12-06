from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

@csrf_exempt
def chat_with_gemini(request):
    if request.method == 'POST':
        try:
            # Get user message from request
            body = json.loads(request.body)
            user_message = body.get('message')

            # Send the message to the Gemini API
            gemini_response = requests.post(
                settings.GEMINI_API_URL,
                headers={
                    'Authorization': f'Bearer {settings.GEMINI_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={"message": user_message}
            )

            # Parse Gemini's response
            gemini_data = gemini_response.json()
            response_message = gemini_data.get('response', "I'm sorry, I couldn't process that.")

            return JsonResponse({'response': response_message})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def chatbot_home(request):
    return render(request, 'chatbot/chat.html')
