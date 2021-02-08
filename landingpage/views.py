from datetime import datetime

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm
from .models import SessionHistory


class login_view(View):
    def get (self, request):
        if request.session.exists(request.session.session_key):
            return redirect('dashboard_view')
        form = LoginForm()
        contex={
                "title": "Login",
                "form": form
                }
        return render(request, 'landingpage/auth-login.html', contex)

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
                return render(request, 'landingpage/auth-login.html', contex)
        messages.error(request, 'Datos no validos.')
        contex = {
                    "title":"Login",
                    "form": form
                }
        return render(request, 'landingpage/auth-login.html', contex)


class Dashboard_view(LoginRequiredMixin, View):
    login_url = 'login_view'
    
    def get (self, request):
        history= SessionHistory.objects.filter(user_sesions=request.user)
        contex={
            "title": "Inicios de sesión", 
            "history": history
            }
        return render(request, 'dashboard/index.html', contex)


class recover_pass(View):
    def post (self, request):
        messages.success(request, 'Se ha enviado un correo electrónico a la dirección solicitada.')
        return redirect('login_view')

def logout_view(request):
    logout(request)
    return redirect('login_view')
