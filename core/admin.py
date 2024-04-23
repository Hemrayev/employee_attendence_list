from django.contrib import admin

from core.models import Staff, GetIn


# Register your models here.

class StaffAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'profession', 'phone_number')
    prepopulated_fields = { 'slug':('fullname',)}

class GetInAdmin(admin.ModelAdmin):
    list_display = ('person_id', 'get_in_date', 'get_in_time', 'in_work')



admin.site.register(Staff,StaffAdmin)
admin.site.register(GetIn,GetInAdmin)
