from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import loginForm


class login_view(View):
    def get (self, request):
        form = loginForm()
        contex={
                "title":"Login",
                "form": form
                }
        return render(request, 'landingpage/auth-login.html', contex)

    def post (self, request):
        return redirect('dashboard_view')


class Dashboard_view(View):
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
