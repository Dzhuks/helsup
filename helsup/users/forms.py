from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import (Client, ClientProfile, CustomUser, Volunteer,
                          VolunteerProfile)


class VolunteerSignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label="Введите пароль еще раз",
        widget=forms.PasswordInput(),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "input_box  "
            field.field.widget.attrs["required"] = "required"

        self.fields['first_name'].widget.input_type = 'text'
        self.fields['email'].widget.input_type = 'text'
        self.fields['phone_number'].widget.input_type = 'tel'

    class Meta(UserCreationForm.Meta):
        model = Volunteer
        fields = ("first_name", "email", "phone_number", "password1", "password2")
        labels = {
            "first_name": "Имя",
            "email": "Эл. почта",
            "phone_number": "Номер телефона",
        }


class ClientSignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label="Введите пароль еще раз",
        widget=forms.PasswordInput(),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "input_box  "
            field.field.widget.attrs["required"] = "required"

        self.fields['first_name'].widget.input_type = 'text'
        self.fields['email'].widget.input_type = 'text'
        self.fields['phone_number'].widget.input_type = 'tel'

    class Meta(UserCreationForm.Meta):
        model = Client
        fields = ("first_name", "email", "phone_number", "password1", "password2")
        labels = {
            "first_name": "Имя",
            "email": "Эл. почта",
            "phone_number": "Номер телефона",
        }


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Эл. почта")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "input_box"
            field.field.widget.attrs["required"] = "required"

        self.fields['email'].widget.input_type = 'text'
        self.fields['password'].widget.input_type = 'password'

    class Meta:
        fields = ("email", "password")


class UpdateCustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "email", "phone_number")


class UpdateVolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = VolunteerProfile
        fields = ['age', 'sex', 'city', 'about_me']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False


class UpdateClientProfileForm(forms.ModelForm):
    mobility = forms.ChoiceField(choices=ClientProfile.Mobility.choices, required=False, label="Мобильность")

    class Meta:
        model = ClientProfile
        fields = ['age', 'sex', 'city', 'about_me', 'mobility']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
