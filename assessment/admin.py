from django.contrib import admin

from .models import Employee, Area, Year, Unit, Desg, Section, Sanction, SanctionSection

# Register your models here.


admin.site.register(Employee)
admin.site.register(Area)
admin.site.register(Year)
# admin.site.register(Unit)
# admin.site.register(Desg)
admin.site.register(Section)
admin.site.register(SanctionSection)

@admin.register(Unit)
class AssessmentUnitAdmin(admin.ModelAdmin):
    list_display = ('u_area', 'u_name', 'u_code','u_type')
    list_filter = ('u_type', 'u_area')
    search_fields = ('u_name__icontains','u_code__icontains', 'u_type__icontains',)

@admin.register(Sanction)
class AssessmentSanctionAdmin(admin.ModelAdmin):
    list_display = ('sn_id', 'sn_dscd', 'sn_unit', 'sn_ext','sn_req', 'sn_san', 'sn_comment')
    search_fields = ('sn_comment__icontains','sn_dscd__d_code__icontains','sn_unit__u_code__icontains',)
    list_filter = ('sn_dscd__d_cadre', 'sn_unit__u_area', )

@admin.register(Desg)
class AssessmentDesgAdmin(admin.ModelAdmin):
    list_display = ('d_id', 'd_code', 'd_name', 'd_grade','d_gdesig', 'd_cadre', 'd_discp', 'd_gcode')
    search_fields = ('d_name__icontains','d_code__icontains',)
    list_filter = (   'd_cadre', 'd_discp','d_grade', 'd_gcode', 'd_gdesig',)
