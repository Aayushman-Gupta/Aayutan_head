import hashlib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from health_app.models import Patient
from .models import ChatSession
from .models import Message
from .serializers import MessageSerializer
from django.views.decorators.csrf import csrf_exempt,csrf_protect

@csrf_exempt
@api_view(['POST'])
def create_chat_session(request):
    username1 = request.data.get('username1')
    username2 = request.data.get('username2')
    print(username1)
    print(username2)
    if not username1 or not username2:
        return Response(data={'error': 'user1 and user2 IDs are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user1 = Patient.objects.get(username=username1)
        user2 = Patient.objects.get(username=username2)
    except Patient.DoesNotExist:
        return Response(data={'error': 'Invalid user1 or user2.'}, status=status.HTTP_404_NOT_FOUND)

    # Generate chat ID
    chat_id = generate_chat_id(user1, user2)

    # Create or retrieve chat session
    chat_session, created = ChatSession.objects.get_or_create(chat_id=chat_id)

    if created:
        return Response(data={'message': 'Chat session created.', 'chat_id': chat_id}, status=status.HTTP_201_CREATED)
    else:
        return Response(data={'message': 'Chat session already exists.', 'chat_id': chat_id}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_chat_messages(request, chat_id):
    chat = ChatSession.objects.get(chat_id=chat_id)
    messages = Message.objects.filter(chat=chat).order_by('created_time')
    serializer = MessageSerializer(messages, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


def generate_chat_id(user1, user2):
    # Ensure consistent ordering to make it independent of who is the user1 or user2
    Patients = sorted([str(user1.username), str(user2.username)])
    combined = "".join(Patients)

    # TODO : Ensure at most 95 characters
    # Create a hash of the combined string
    chat_id = hashlib.sha256(combined.encode()).hexdigest()
    return chat_id
