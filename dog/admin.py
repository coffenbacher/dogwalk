from django.contrib import admin
from models import *
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

class WalkerAdmin(admin.ModelAdmin):
    hidden = ['node']

class DogAdmin(admin.ModelAdmin):
    hidden = ['node']

class RequiredWalkAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

admin.site.register(Dog, DogAdmin)
admin.site.register(Walker, WalkerAdmin)
admin.site.register(RequiredWalk, RequiredWalkAdmin)
