from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from models import *
from django import forms

class ScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = Schedule
        widgets = {
            'walkers': FilteredSelectMultiple('Walkers', False, choices=Walker.objects.all()),
            'dogs': FilteredSelectMultiple('Dogs', False, choices=Dog.objects.all()),
        }
        exclude = ['problem', 'solutions', 'schedule']
    
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleAdminForm

admin.site.register(Schedule, ScheduleAdmin)
