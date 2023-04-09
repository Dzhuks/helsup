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
