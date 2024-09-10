from rest_framework_simplejwt.tokens import RefreshToken
from .models import Patient


def get_token_for_user(user: Patient):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }
