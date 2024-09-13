import hashlib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from health_app.models import Patient
from .models import ChatSession
from .models import Message
from .serializers import MessageSerializer
from django.views.decorators.csrf import csrf_exempt
from .utils.getChatId import generate_chat_id
from Aayutan.utils.api_response import ApiResponse


@csrf_exempt
@api_view(['POST'])
def create_chat_session(request):
    username1 = request.data.get('username1')
    username2 = request.data.get('username2')
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
        response = ApiResponse(
            status='success',
            data={'chat_id': chat_id},
            message='Chat session created.',
            status_code=201
        )
        return Response(data=response.to_dict(), status=status.HTTP_201_CREATED)
    else:
        response = ApiResponse(
            status='success',
            data={'chat_id': chat_id},
            message='Chat session already exists.',
            status_code=200
        )
        return Response(data=response.to_dict(), status=status.HTTP_200_OK)


@api_view(['GET'])
def get_chat_messages(request, chat_id):
    chat = ChatSession.objects.get(chat_id=chat_id)
    messages = Message.objects.filter(chat=chat).order_by('created_time')
    serializer = MessageSerializer(messages, many=True)
    response = ApiResponse(
        status='success',
        status_code=200,
        data=serializer.data
    )
    return Response(data=response.to_dict(), status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_chat_session(request, chat_id):
    chat = ChatSession.objects.get(chat_id=chat_id)
    chat.delete()
    response = ApiResponse(
        status='success',
        status_code=200,
        message='Chat deleted successfully'
    )
    return Response(data=response.to_dict(), status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()
    response = ApiResponse(
        status='success',
        status_code=200,
        message='Message deleted successfully'
    )
    return Response(data=response.to_dict(), status=status.HTTP_200_OK)
