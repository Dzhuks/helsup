from django.contrib import admin
from users.models import ClientProfile, CustomUser, VolunteerProfile

admin.site.register(CustomUser)
admin.site.register(VolunteerProfile)
admin.site.register(ClientProfile)
