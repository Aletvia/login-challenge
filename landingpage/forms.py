from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import SessionHistory

"""
Formulario para inicio de sesión.
"""
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=5, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nombre de usuario"}))
    password = forms.CharField(max_length=32, min_length=8, widget=forms.PasswordInput(attrs={'class': "form-control", "placeholder": "Contraseña"}))


"""
Formulario de correo para recuperación de contraseña.
send_email envía un correo al usuario para que pueda reestablecer su contraseña
"""
class EmailForm(forms.Form):
    email = forms.EmailField(max_length=40, min_length=9, widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "Correo"}))

    def send_email(self, user_recover):
        msj = """\
                <html>
                <head></head>
                <body>
                    <h3>Hola {name}</h3>
                    <p>Hemos recibido una solicitud para recuperación de contraseña. <br>
                        Si haz sido tú ingresa al siguiente link:<br>
                        <a href="{host}recover-password/{id}">Recuperar contraseña</a><br>
                        De lo contrario ignora este correo.
                    </p>
                </body>
                </html>"""
        try:
                subject, from_email, to = 'Recuperar contraseña', settings.EMAIL_HOST_USER, user_recover.email
                text_content = 'Hola '+user_recover.username
                html_content = msj.format(name=user_recover.username, host=settings.URL_HOST, id=str(user_recover.id))
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return{
                    'type':'success',
                    'msj':'Se ha enviado un correo electrónico a la dirección solicitada.'
                    }
        except:
                return{
                    'type':'error',
                    'msj':'Hubo un problema al enviar el correo, favor de intentar más tarde.'
                    }


"""
Formulario para actualizar contraseña.
"""
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(max_length=30, min_length=8, widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Nueva contraseña"}))