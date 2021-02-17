from django.core.mail import EmailMultiAlternatives

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin

from .forms import LoginForm, EmailForm, ChangePasswordForm
from .models import SessionHistory


"""
Class View para inicio de sesión.
"""
class LoginView(View):
    def get (self, request):
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
class DashboardView(LoginRequiredMixin, ListView):
    login_url = 'login_view'
    redirect_field_name = 'redirect_to'
    model = SessionHistory
    template_name = 'dashboard/index.html'
    context_object_name = 'history'
    
    def get_queryset(self):
        dt =  self.request.GET.get('date_search', None)
        if dt:
            return SessionHistory.objects.filter(user_sesions=self.request.user, date_login=dt)
        else:
            return SessionHistory.objects.filter(user_sesions=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Inicios de sesión"
        return context


"""
Class View para recuperar contraseña.
"""
class UserChangePassword(SuccessMessageMixin, View):
    login_url = 'login_view'
    redirect_field_name = 'redirect_to'

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
            try:
                user_recover= User.objects.get(email=email)
                result = form.send_email(user_recover)
                if result['type']=='error':
                    messages.error(request, result['msj'])
                else:
                    messages.success(request, result['msj'])
                return redirect('login_view')
            except:
                messages.error(request, 'Correo no válido.')
                return redirect('login_view')
        else:
            messages.error(request, 'Formato de correo no válido.')
            return redirect('login_view')


"""
Función para cerrar sesión.
"""
def LogoutView(request):
    logout(request)
    return redirect('login_view')
