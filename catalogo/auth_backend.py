import os
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class DevAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        if os.environ.get('DISABLE_AUTH', 'False') != 'False':
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
