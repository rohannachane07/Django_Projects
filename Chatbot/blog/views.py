from django.shortcuts import render
from django.http import HttpResponse
from .models import Message

def index(request):
    return render(request, 'blog/index.html')

def getResponse(request):
    if request.method == 'GET':
        user_message = request.GET.get('userMessage')
        try:
            message = Message.objects.get(text=user_message)
            response_message = message.response
        except Message.DoesNotExist:
            response_message = "Sorry, I couldn't understand that."

        return HttpResponse(response_message)
    else:
        return HttpResponse('Invalid request method', status=400)
