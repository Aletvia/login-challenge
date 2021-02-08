from django import forms
from django.forms import ModelForm

from .models import SessionHistory

"""
Formulario para inicio de sesión.
"""
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=5, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nombre de usuario"}))
    password = forms.CharField(max_length=32, min_length=8, widget=forms.PasswordInput(attrs={'class': "form-control", "placeholder": "Contraseña"}))


"""
Formulario de correo para recuperación de contraseña.
"""
class EmailForm(forms.Form):
    email = forms.EmailField(max_length=40, min_length=9, widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "Correo"}))


"""
Formulario para actualizar contraseña.
"""
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(max_length=30, min_length=8, widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Nueva contraseña"}))