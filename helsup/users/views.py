from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import (CustomLoginForm, SignUpForm, UpdateClientProfileForm,
                         UpdateCustomUserForm, UpdateVolunteerProfileForm)
from users.models import CustomUser


# Sign Up View
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


class UserLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "users/login.html"

    def form_valid(self, form):
        return super(UserLoginView, self).form_valid(form)


@login_required
def logout(request):
    django_logout(request)
    return redirect('homepage:home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateCustomUserForm(request.POST, instance=request.user)
        if request.user.role == CustomUser.Roles.VOLUNTEER:
            profile_form = UpdateVolunteerProfileForm(request.POST, request.FILES, instance=request.user.profile)
        else:
            profile_form = UpdateClientProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, 'Your profile is updated successfully')
            return redirect('homepage:home')
    else:
        user_form = UpdateCustomUserForm(instance=request.user)
        if request.user.role == CustomUser.Roles.VOLUNTEER:
            profile_form = UpdateVolunteerProfileForm(instance=request.user.profile)
        else:
            profile_form = UpdateClientProfileForm(instance=request.user.profile)

    template_name = "users/profile.html"
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, template_name, context)
