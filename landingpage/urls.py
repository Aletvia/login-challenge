from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login_view.as_view(), name='login_view'),
    path('dashboard', Dashboard_view.as_view(), name='dashboard_view'),
    path('recover', recover_pass.as_view(), name='recover_pass'),
    path('logout', logout_view,  name='logout_view'),
]


