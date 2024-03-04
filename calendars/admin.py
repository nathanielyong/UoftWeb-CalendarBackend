from django.contrib import admin
from .models import Calendar, Event

admin.site.register(Calendar)
admin.site.register(Event)