import hashlib
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from health_app.models import Patient
from .models import ChatSession


@api_view(['POST'])
def create_chat_session(request):
    username1 = request.data.get('username1')
    username2 = request.data.get('username2')
    print(username1)
    print(username2)
    if not username1 or not username2:
        return JsonResponse({'error': 'user1 and user2 IDs are required.'}, status=400)

    try:
        user1 = Patient.objects.get(username=username1)
        user2 = Patient.objects.get(username=username2)
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Invalid user1 or user2.'}, status=404)

    # Generate chat ID
    chat_id = generate_chat_id(user1, user2)

    # Create or retrieve chat session
    chat_session, created = ChatSession.objects.get_or_create(chat_id=chat_id)

    if created:
        return JsonResponse({'message': 'Chat session created.', 'chat_id': chat_id}, status=201)
    else:
        return JsonResponse({'message': 'Chat session already exists.', 'chat_id': chat_id}, status=200)


def generate_chat_id(user1, user2):
    # Ensure consistent ordering to make it independent of who is the user1 or user2
    Patients = sorted([str(user1.username), str(user2.username)])
    combined = "".join(Patients)
    # Create a hash of the combined string
    chat_id = hashlib.sha256(combined.encode()).hexdigest()
    return chat_id
