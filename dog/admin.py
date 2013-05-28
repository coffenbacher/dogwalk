from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from models import *
from django import forms
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

class DogAdminForm(forms.ModelForm):
    class Meta:
        model = Dog
        widgets = {
            'incompatible': FilteredSelectMultiple('Dogs', False, choices=Dog.objects.all()),
        }
        exclude = ['node']

class PreferredWalkerAdmin(admin.ModelAdmin):
    pass

class WalkerAdmin(admin.ModelAdmin):
    exclude = ['node']

class DogAdmin(admin.ModelAdmin):
    form = DogAdminForm

class RequiredWalkAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

class CancelledWalkAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }



admin.site.register(Dog, DogAdmin)
admin.site.register(Walker, WalkerAdmin)
admin.site.register(RequiredWalk, RequiredWalkAdmin)
admin.site.register(CancelledWalk, CancelledWalkAdmin)
admin.site.register(PreferredWalker, PreferredWalkerAdmin)
