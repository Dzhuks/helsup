from django.urls import path
from users.views import (ClientSignUpView, UserLoginView, VolunteerSignUpView,
                         choice, logout, profile)

app_name = "users"

urlpatterns = [
    path("choice/", choice, name="choice"),
    path("signup/volunteer", VolunteerSignUpView.as_view(), name="vol_signup"),
    path("signup/client", ClientSignUpView.as_view(), name="cli_signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('logout/', logout, name='logout'),
    path("profile/", profile, name="profile"),
]
