from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import (MOBILITY_CHOICES, SEX_CHOICES, BaseProfile,
                          ClientProfile, CustomUser, Volunteer,
                          VolunteerProfile)


class SignUpForm(UserCreationForm):
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


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "input_box"
            field.field.widget.attrs["required"] = "required"

        self.fields['username'].widget.input_type = 'text'
        self.fields['password'].widget.input_type = 'password'

    class Meta:
        model = CustomUser
        fields = ("username", "password")
        labels = {
            'username': "Эл. почта",
            "password": "Пароль",
        }


class UpdateCustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "email", "phone_number")


class BaseUpdateProfileForm(forms.ModelForm):
    image = forms.ImageField(
        label="картинка",
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
        required=False,
        help_text='загрузите ваше лицо для вызова доверия среди пользователей'
    )
    age = forms.IntegerField(
        label="возраст",
        min_value=14, max_value=130,
        required=False,
    )
    sex = forms.ChoiceField(
        label="пол",
        choices=SEX_CHOICES,
        required=False,
    )

    class Meta:
        model = BaseProfile
        exclude = ("rating",)


class UpdateVolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = VolunteerProfile
        exclude = ("rating", "user", "image")


class UpdateClientProfileForm(forms.ModelForm):
    mobility = forms.ChoiceField(
        label="мобильность",
        choices=MOBILITY_CHOICES,
    )

    class Meta:
        model = ClientProfile
        exclude = ("rating", "user", "image")
