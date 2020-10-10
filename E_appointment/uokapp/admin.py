from django.contrib import admin
from uokapp.models import appointment, student, staffs, othersuggestion
# Register your models here.

admin.site.register(appointment)
admin.site.register(student)
admin.site.register(staffs)
admin.site.register(othersuggestion)
