from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from models import *
from django import forms

class PlanAdminForm(forms.ModelForm):
    class Meta:
        model = Plan
        widgets = {
            'walkers': FilteredSelectMultiple('Walkers', False, choices=Walker.objects.all()),
            'dogs': FilteredSelectMultiple('Dogs', False, choices=Dog.objects.all()),
        }
        exclude = ['problem', 'solutions', 'schedule']
    
class PlanAdmin(admin.ModelAdmin):
    form = PlanAdminForm

admin.site.register(Plan, PlanAdmin)
