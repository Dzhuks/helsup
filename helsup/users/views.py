from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View
from users.forms import (LoginForm, SignUpForm, UpdateCustomUserForm,
                         UpdateProfileForm)


class SignUpView(View):
    form_class = SignUpForm
    initial = {"key": "value"}
    template_name = "users/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("homepage:home")
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            # first_name = form.cleaned_data.get("first_name")
            # messages.success(request, f"Аккаунт {first_name} успешно создан")
            return redirect("users:login")

        return render(request, self.template_name, {"form": form})


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(UserLoginView, self).form_valid(form)


@login_required
def logout(request):
    django_logout(request)
    return redirect('homepage:home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateCustomUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, 'Your profile is updated successfully')
            return redirect('homepage:home')
    else:
        user_form = UpdateCustomUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    template_name = "users/profile.html"
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, template_name, context)
