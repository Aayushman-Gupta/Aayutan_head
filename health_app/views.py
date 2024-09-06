# # from django.http import JsonResponse
# import json
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework_simplejwt.exceptions import TokenError
# from django.contrib.auth import authenticate
# # from .models import Patient

# from .forms import PatientForm

    # @csrf_exempt
    # def register(request):
    #     if request.method == 'POST':
    #         try:
    #             data = json.loads(request.body)
    #             form = PatientForm(data)
    #             if form.is_valid():
    #                 patient = form.save()

    #                 # Generate token
    #                 refresh = RefreshToken.for_user(patient)

    #                 return Response({
    #                     'message': 'User registered successfully',
    #                     'refresh': str(refresh),
    #                     'access': str(refresh.access_token),
    #                 }, status=201)
    #             else:
    #                 return Response({'errors': form.errors}, status=400)
    #         except json.JSONDecodeError:
    #             return Response({'error': 'Invalid JSON'}, status=400)
    #     else:
    #         return Response({'error': 'Invalid HTTP method'}, status=405)

# @csrf_exempt
# def login(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')
#             password = data.get('password')

#             # Authenticate the user
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 # Generate tokens
#                 refresh = RefreshToken.for_user(user)
#                 return JsonResponse({
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }, status=200)
#             else:
#                 return JsonResponse({'error': 'Invalid credentials'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'POST request required'}, status=405)
    
# @csrf_exempt   
# def logout(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             refresh_token = data.get('refresh_token')

#             try:
#                 token = RefreshToken(refresh_token)
#                 token.blacklist()

#                 return JsonResponse({'message': 'Successfully logged out'}, status=200)
#             except TokenError:
#                 return JsonResponse({'error': 'Invalid token'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'POST request required'}, status=405)