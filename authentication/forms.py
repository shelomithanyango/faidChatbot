from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import validate_not_disposable_email


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(
        validators=[validate_not_disposable_email],
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': ' '})
    )

    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': ' '})
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': ' '})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': ' '})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': ' '})
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "phone_number",
            "password1",
            "password2"
        )