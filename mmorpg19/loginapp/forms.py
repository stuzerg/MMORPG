import django.db.models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.forms import ModelForm

class UserTryingLog(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

