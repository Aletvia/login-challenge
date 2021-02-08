from django.db import models
from django.contrib.auth.models import User

class SessionHistory(models.Model):
    date_login = models.DateField(auto_now_add=True)
    time_login = models.TimeField(auto_now_add=True)
    user_sesions = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sessions')


