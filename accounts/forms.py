from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class LoginForm(AuthenticationForm):
    """Вход по логину или по email."""

    username = forms.CharField(
        label='Логин или email',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'Логин или email',
        })
    )

    def clean_username(self):
        value = self.cleaned_data['username']

        if '@' in value:
            match = User.objects.filter(email__iexact=value).first()
            if match:
                return match.get_username()

        return value


class SignupForm(UserCreationForm):
    """Регистрация. Email обязателен и должен быть уникальным."""

    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'})
    )

    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Как к вам обращаться'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже зарегистрирован.'
            )

        return email