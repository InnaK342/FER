from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Photo


class PhotoForm(forms.Form):
    photo = forms.FileField(label='Фото', widget=forms.FileInput(attrs={'class': 'form-control'}))
    # class Meta:
    #     model = Photo
    #     fields = ['photo']
    #     widgets = {'photo': forms.FileInput(attrs={'class': "form-control"})}


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Електронна пошта')
    username = forms.CharField(label='Ім\'я користувача')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=255, label='Ім\'я')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)