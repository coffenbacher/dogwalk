from django.contrib import admin
from models import *

class WeekAdmin(admin.ModelAdmin):
    exclude = ['problem', 'solutions', 'schedule']


admin.site.register(Week, WeekAdmin)
