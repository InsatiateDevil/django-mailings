from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, EmailField, EmailInput, ModelForm
from mailing.forms import StyleFormMixin
from users.models import User


class LoginForm(Form):
    email = forms.EmailField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'password']


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserUpdateForm(StyleFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'phone_number', 'avatar']


class PasswordRecoveryForm(Form):
    email = EmailField(
        required=True,
        widget=EmailInput(
            attrs={
                'placeholder': 'Введите адрес электронной почты',
                'class': 'form-control text-center',
            }
        ),
    )
