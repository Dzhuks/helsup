from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView
from users.decorators import client_required, volunteer_required
from users.forms import (ClientSignUpForm, UpdateClientProfileForm,
                         UpdateCustomUserForm, UpdateVolunteerProfileForm,
                         UserLoginForm, VolunteerSignUpForm)
from users.models import Client, Volunteer


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
                if isinstance(user, Volunteer):
                    return redirect("orders:show_orders")
                elif isinstance(user, Client):
                    return redirect("orders:my_orders")
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }
    return render(request, template_name, context)


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    user_form_class = UpdateCustomUserForm
    profile_form_class = None
    template_name = "users/profile.html"
    redirect_url = None

    def get_user_profile(self, request):
        user = request.user
        profile = user.profile
        return user, profile

    def get(self, request):
        user, profile = self.get_user_profile(request)
        user_form = self.user_form_class(instance=user)
        profile_form = self.profile_form_class(instance=profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user, profile = self.get_user_profile(request)
        user_form = self.user_form_class(request.POST, instance=user)
        profile_form = self.profile_form_class(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(self.redirect_url)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)


@method_decorator(volunteer_required, name="dispatch")
class VolunteerProfileView(ProfileView):
    profile_form_class = UpdateVolunteerProfileForm
    redirect_url = 'orders:show_orders'


@method_decorator(client_required, name="dispatch")
class ClientProfileView(ProfileView):
    profile_form_class = UpdateClientProfileForm
    redirect_url = 'orders:my_orders'
