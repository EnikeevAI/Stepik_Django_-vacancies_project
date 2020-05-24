from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User

from .models import Application

class UserAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Логин',
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputLogin'}
        )
    )
    password = forms.CharField(
        label=("Пароль"),
        widget=forms.PasswordInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputPassword'}
        )
    )


class UserRegisterForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputLogin'}
        )
    )
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputName'}
        )
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputSurname'}
        )
    )
    password = forms.CharField(
        label=("Пароль"),
        widget=forms.PasswordInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputPassword'}
        )
    )


    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name',)


class UserApplicationForm(forms.Form):
    username = forms.CharField(
        label='Вас зовут',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'userName',
                'placeholder': ''}
        )
    )
    userphone = forms.CharField(
        label='Ваш телефон',
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'form-control',
                'id': 'userPhone',
                'placeholder': ''}
        )
    )
    usermsg = forms.CharField(
        label='Сопроводительное письмо',
        widget=forms.Textarea(
            attrs={
                'rows': '8',
                'class': 'form-control',
                'id': 'userЬып',
                }
        )
    )

    class Meta:
        model = Application
        fields = ('username', 'userphone', 'usermsg',)
