from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .forms import LoginForm, EmailForm, ChangePasswordForm
from .models import SessionHistory


"""
Class View para inicio de sesión.
"""
class LoginView(View):
    def get (self, request):
        print()
        if request.session.exists(request.session.session_key):
            return redirect('dashboard_view')
        form = LoginForm()
        contex={
                "title": "Login",
                "form": form
                }
        return render(request, 'landingpage/auth_login.html', contex)

    def post (self, request):
        next = self.request.GET.get('next', '/dashboard')
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                SessionHistory.objects.create(user_sesions=user)
                login(request, user)
                return redirect(next)
            else:
                messages.error(request, 'Usuario o contraseña no validos.')
                contex = {
                    "title":"Login",
                    "form": form
                    }
                return render(request, 'landingpage/auth_login.html', contex)
        messages.error(request, 'Datos no validos.')
        contex = {
                    "title":"Login",
                    "form": form
                }
        return render(request, 'landingpage/auth_login.html', contex)


"""
Class View del historial de sesiones del usuario.
"""
class DashboardView(LoginRequiredMixin, View):
    login_url = 'login_view'
    
    def get (self, request):
        history= SessionHistory.objects.filter(user_sesions=request.user)
        contex={
            "title": "Inicios de sesión", 
            "history": history
            }
        return render(request, 'dashboard/index.html', contex)
        
    def post (self, request):
        dt=request.POST.get('date_search')
        print(dt)
        history= SessionHistory.objects.filter(user_sesions=request.user, date_login=dt)
        contex={
            "title": "Inicios de sesión", 
            "history": history
            }
        return render(request, 'dashboard/index.html', contex)

"""
Class View para recuperar contraseña.
"""
class UserChangePassword(View):

    def get (self, request,pk):
        if request.session.exists(request.session.session_key):
            logout(request)
        form = ChangePasswordForm()
        contex={
                "title": "Recuperar contraseña",
                "form": form
                }
        return render(request, 'landingpage/recover_password.html', contex)

    def post (self, request, pk):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password1']
            u = User.objects.get(id=pk)
            u.set_password(new_password)
            u.save()
            messages.success(request, 'Su contraseña ha sido actualizada.')
            return redirect('login_view')
        else:
            messages.error(request, 'Datos no validos.')
            return redirect('login_view')


"""
Class View para envio de correo por contraseña.
"""
class RecoverPass(View):
    def post (self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_recover= User.objects.get(email=email)
            msj = 'Hola, hemos recibido una solicitud para recuperación de contraseña. Si haz sido tú ingresa al siguiente link:<a href="http://127.0.0.1:8000/recover-password/'+ str(user_recover.id)+ '">Click</a>'
            print(user_recover.password)
            try:
                send_mail(
                    'Recuperar contraseña',
                    msj,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                messages.success(request, 'Se ha enviado un correo electrónico a la dirección solicitada.')
                return redirect('login_view')
            except:
                messages.error(request, 'Hubo un problema al enviar el correo, favor de intentar más tarde.')
                return redirect('login_view')
        else:
            messages.error(request, 'Correo no válido.')
            return redirect('login_view')
        messages.error(request, 'Datos no validos.')
        return redirect('login_view')


"""
Función para cerrar sesión.
"""
def LogoutView(request):
    logout(request)
    return redirect('login_view')
