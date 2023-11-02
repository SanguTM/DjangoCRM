from .models import Room

#sukuriame custom tagus templaitui
def chat_waiting(request):
    waiting_chat = Room.objects.filter(status='waiting')

    return {'waiting_chat': waiting_chat}