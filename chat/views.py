from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from health_app.models import Patient
from .models import ChatSession

@require_POST
def create_chat_session(request):
    sender_username = request.POST.get('sender_username')
    receiver_username = request.POST.get('receiver_username')

    if not sender_username or not receiver_username:
        return JsonResponse({'error': 'Sender and receiver IDs are required.'}, status=400)

    try:
        sender = Patient.objects.get(username=sender_username)
        receiver = Patient.objects.get(username=receiver_username)
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Invalid sender or receiver.'}, status=404)

    # Generate chat ID
    chat_id = generate_chat_id(sender, receiver)

    # Create or retrieve chat session
    chat_session, created = ChatSession.objects.get_or_create(chat_id=chat_id)

    if created:
        return JsonResponse({'message': 'Chat session created.', 'chat_id': chat_id}, status=201)
    else:
        return JsonResponse({'message': 'Chat session already exists.', 'chat_id': chat_id}, status=200)




import hashlib

def generate_chat_id(sender, receiver):
    # Ensure consistent ordering to make it independent of who is the sender or receiver
    Patients = sorted([str(sender.id), str(receiver.id)])
    combined = "".join(Patients)
    # Create a hash of the combined string
    chat_id = hashlib.sha256(combined.encode()).hexdigest()
    return chat_id

    
       
   
    

    