from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class DevAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not settings.DEBUG:
            return None
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None
