from django.db import models
from django.contrib.auth.models import User


class Calendar(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField(default=30)
    last_modified = models.DateTimeField(auto_now=True)
    calendar = models.ForeignKey(
        Calendar, on_delete=models.CASCADE, related_name='events')
