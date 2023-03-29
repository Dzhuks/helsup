from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import MOBILITY_CHOICES, SEX_CHOICES, CustomUser, Profile


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "email", "phone_number", "password")
        labels = {
            "first_name": "Имя",
            "email": "Электронная почта",
            "phone_number": "Номер телефона",
            "password": "Пароль",
        }


class LoginForm(AuthenticationForm):
    email = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "input_box",
            'type': 'text',
            "required": "required"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "input_box",
            'type': "password",
            "required": "required"
        })
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password")


class UpdateCustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "email", "phone_number")


class UpdateProfileForm(forms.ModelForm):
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
    mobility = forms.ChoiceField(
        label="мобильность",
        choices=MOBILITY_CHOICES,
    )

    class Meta:
        model = Profile
        exclude = ("rating",)
