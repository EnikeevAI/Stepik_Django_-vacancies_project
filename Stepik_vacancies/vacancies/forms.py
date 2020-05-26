from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User

from .models import Application, Company



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
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputPassword'}
        )
    )


class UserCompanyEditForm(forms.ModelForm):
    name = forms.CharField(
        max_length=64,
        label='Название компании',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'companyName',
                'type': 'text',
                }
        )
    )
    location = forms.CharField(
        max_length=64,
        label='География',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'companyLocation',
                'type': 'text'
                }
        )
    )
    logo = forms.FileField(
        label='Логотип',
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'id': 'inputGroupFile01',

            }
        )
    )
    description = forms.CharField(
        max_length=200,
        label='Информация о компании',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'companyInfo',
                'rows': '4',
                'style': 'color:#000;'
                }
        )
    )
    employee_count = forms.IntegerField(
        label='Количество человек в компании',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'companyTeam',
                }
        )
    )


    class Meta:
        model = Company
        fields = ('name', 'location', 'logo', 'description', 'employee_count',)



class UserRegisterForm(forms.ModelForm):
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
        label="Пароль",
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


class UserApplicationForm(forms.ModelForm):
    written_username = forms.CharField(
        max_length=64,
        label='Вас зовут',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'userName',
                'placeholder': ''}
        )
    )
    written_phone = forms.CharField(
        max_length=64,
        label='Ваш телефон',
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'form-control',
                'id': 'userPhone',
                'placeholder': ''}
        )
    )
    written_cover_letter = forms.CharField(
        max_length=500,
        label='Сопроводительное письмо',
        widget=forms.Textarea(
            attrs={
                'rows': '8',
                'class': 'form-control',
                'id': 'userMsg',
                }
        )
    )


    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter',)

