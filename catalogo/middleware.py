import os
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import login

class AutoLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if os.environ.get('DISABLE_AUTH', 'False') == 'True':
            if not request.user.is_authenticated:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    user = User.objects.get(username='admin')
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                except User.DoesNotExist:
                    pass
