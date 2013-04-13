from django.contrib import admin
from models import *
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

class RequiredWalkAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

admin.site.register(Dog)
admin.site.register(Walker)
admin.site.register(RequiredWalk, RequiredWalkAdmin)
