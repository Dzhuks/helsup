from django import forms
from users.models import MOBILITY_CHOICES, SEX_CHOICES, CustomUser, Profile


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "input_box"
            field.field.widget.attrs["required"] = "required"

        self.fields['first_name'].widget.attrs['type'] = 'text'
        self.fields['email'].widget.attrs['type'] = 'text'
        self.fields['phone_number'].widget.attrs['type'] = 'tel'
        self.fields['password'].widget.attrs['type'] = 'password'

    class Meta:
        model = CustomUser
        fields = ("first_name", "email", "phone_number", "password")
        labels = {
            "first_name": "Имя",
            "email": "Эл. почта",
            "phone_number": "Номер телефона",
            "password": "Пароль",
        }


class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "input_box"
            field.field.widget.attrs["required"] = "required"

        self.fields['email'].widget.attrs['type'] = 'text'
        self.fields['password'].widget.attrs['type'] = 'password'

    class Meta:
        model = CustomUser
        fields = ("email", "password")
        labels = {
            'email': "Эл. почта",
            "password": "Пароль",
        }


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
