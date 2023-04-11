from django.contrib.auth.backends import ModelBackend
from users.models import Client, Volunteer


class VolunteerAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            volunteer = Volunteer.objects.get(email=email)
        except Volunteer.DoesNotExist:
            return None

        if volunteer.check_password(password):
            return volunteer
        else:
            return None

    def get_user(self, user_id):
        try:
            return Volunteer.objects.get(pk=user_id)
        except Volunteer.DoesNotExist:
            return None


class ClientAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            return None

        if client.check_password(password):
            return client
        else:
            return None

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return None
