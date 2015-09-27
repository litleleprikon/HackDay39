from django.contrib.auth.models import User
from django.db import models


class Activity(models.Model):
    limit = models.IntegerField()
    gone_time = models.IntegerField(default=0)
    user = models.ForeignKey(User)


class Link(Activity):
    url = models.URLField(unique=True)


class Game(Activity):
    name = models.URLField(unique=True)
