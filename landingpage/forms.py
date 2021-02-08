from django import forms

from .models import SessionHistory

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=5, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nombre de usuario"}))
    password = forms.CharField(max_length=32, min_length=8, widget=forms.PasswordInput(attrs={'class': "form-control", "placeholder": "Contraseña"}))