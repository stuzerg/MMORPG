from random import random, randint

from django.contrib.auth.models import User
from django.db import models


class verificationtable(models.Model):
    mailbox = models.CharField(max_length=255, unique=True)
    vcode = models.CharField(max_length=4)
    vtime = models.DateTimeField()
    vname = models.CharField(max_length=255)
    vpass = models.CharField(max_length=255)


# Create your models here.
