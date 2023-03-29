from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import MOBILITY_CHOICES, SEX_CHOICES, CustomUser, Profile


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

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
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = CustomUser
        fields = ("first_name", "password", "remember_me")


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
