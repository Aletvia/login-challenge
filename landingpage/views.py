from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import loginForm


class login_view(View):
    def get (self, request):
        if request.session.exists(request.session.session_key):
            return redirect('dashboard_view')
        form = loginForm()
        contex={
                "title":"Login",
                "form": form
                }
        return render(request, 'landingpage/auth-login.html', contex)

    def post (self, request):
        next = self.request.GET.get('next', '/dashboard')
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
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
        contex={"title":"Inicios de sesión"}
        return render(request, 'dashboard/index.html', contex)


class recover_pass(View):
    def post (self, request):
        messages.success(request, 'Se ha enviado un correo electrónico a la dirección solicitada.')
        return redirect('login_view')

def logout_view(request):
    logout(request)
    return redirect('login_view')
