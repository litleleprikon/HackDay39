from django.contrib.auth.models import User
from django.db import models


class Activity(models.Model):
    limit = models.IntegerField()
    gone_time = models.IntegerField(default=0)
    user = models.ForeignKey(User)


class Link(Activity):
    url = models.TextField(unique=True)


class Game(Activity):
    name = models.TextField(unique=True)


# class ExecutedActivity(models.Model):
#     activity = models.ForeignKey(Activity)
#     time = models.DateTimeField(auto_now=True)


class LastActivity(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)


class LastProgram(LastActivity):
    activity = models.ForeignKey(Game, null=True)


class LastSite(LastActivity):
    activity = models.ForeignKey(Link, null=True)


