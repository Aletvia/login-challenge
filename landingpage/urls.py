from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login_view'),
    path('logout', LogoutView,  name='logout_view'),
    path('mail-recover', RecoverPass.as_view(), name='recover_pass'),
    path('recover-password/<int:pk>', UserChangePassword.as_view(), name='change_pass'),
    path('dashboard', DashboardView.as_view(), name='dashboard_view'),
]


