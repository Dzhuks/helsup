from django.urls import path
from users.views import SignUpView, UserLoginView, logout, profile

app_name = "users"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('logout/', logout, name='logout'),
    path("profile/", profile, name="profile"),
]
