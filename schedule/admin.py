from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from models import *

class WeekAdmin(admin.ModelAdmin):
    exclude = ['problem', 'solutions', 'schedule']
    formfield_overrides = {
            models.ManyToManyField: {'widget': FilteredSelectMultiple },
    }

admin.site.register(Week, WeekAdmin)
