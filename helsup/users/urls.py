from django.urls import path
from users.views import (ClientProfileView, ClientSignUpView,
                         VolunteerProfileView, VolunteerSignUpView, choice,
                         login_view, logout_view)

app_name = "users"

urlpatterns = [
    path("choice/", choice, name="choice"),

    path('volunteer/signup/', VolunteerSignUpView.as_view(), name='vol_signup'),
    path('client/signup/', ClientSignUpView.as_view(), name='cli_signup'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path("volunteer/profile", VolunteerProfileView.as_view(), name="vol_profile"),
    path("client/profile", ClientProfileView.as_view(), name="cli_profile"),
]
