from django.contrib import admin

from .models import Employee, Area, Year, Unit, Desg, Section, Sanction, SanctionSection

# Register your models here.


admin.site.register(Employee)
admin.site.register(Area)
admin.site.register(Year)
admin.site.register(Unit)
admin.site.register(Desg)
admin.site.register(Section)
admin.site.register(Sanction)
admin.site.register(SanctionSection)
