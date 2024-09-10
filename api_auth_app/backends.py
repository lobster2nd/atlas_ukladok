from django.db.models import Q

from api_profile_app.models import User


class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_uid):
        try:
            return User.objects.get(pk=user_uid)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username) | Q(phone=username)
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            return None