from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from users.backends import ClientAuthBackend, VolunteerAuthBackend
from users.forms import (ClientSignUpForm, UpdateClientProfileForm,
                         UpdateCustomUserForm, UpdateVolunteerProfileForm,
                         UserLoginForm, VolunteerSignUpForm)
from users.models import Client, Volunteer, VolunteerProfile


# Sign Up Views
class VolunteerSignUpView(CreateView):
    form_class = VolunteerSignUpForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


class ClientSignUpView(CreateView):
    form_class = ClientSignUpForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


def choice(request):
    template_name = "users/choice.html"
    context = {}
    return render(request, template_name, context)


@login_required
def logout_view(request):
    django_logout(request)
    return redirect('homepage:home')


def login_view(request):
    template_name = "users/login.html"
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("orders:show_orders")
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required
def profile(request):
    print(request.user.__class__)
    if request.method == 'POST':
        user_form = UpdateCustomUserForm(request.POST, instance=request.user)
        if isinstance(request.user, Volunteer):
            profile_form = UpdateVolunteerProfileForm(request.POST, request.FILES, instance=request.user.profile)
        elif isinstance(request.user, Client):
            profile_form = UpdateClientProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, 'Your profile is updated successfully')
            return redirect('orders:show_orders')
        else:
            user_form = UpdateCustomUserForm(instance=request.user)
            if isinstance(request.user, Volunteer):
                profile_form = UpdateVolunteerProfileForm(request.POST, request.FILES, instance=request.user.profile)
            elif isinstance(request.user, Client):
                profile_form = UpdateClientProfileForm(request.POST, request.FILES, instance=request.user.profile)
    else:
        user_form = UpdateCustomUserForm(instance=request.user)
        if isinstance(request.user, Volunteer):
            vol_profile = VolunteerProfile.objects.get(volunteer=request.user)
            profile_form = UpdateVolunteerProfileForm(request.POST, request.FILES, instance=vol_profile)
        elif isinstance(request.user, Client):
            profile_form = UpdateClientProfileForm(request.POST, request.FILES, instance=request.user.profile)

    template_name = "users/profile.html"
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, template_name, context)
