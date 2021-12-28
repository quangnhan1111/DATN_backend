from django.contrib import admin

# Register your models here.
from mailer.models import ScheduleMail

admin.site.register(ScheduleMail)