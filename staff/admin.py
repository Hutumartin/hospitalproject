from django.contrib import admin
from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'specialization', 'phone', 'email')
    search_fields = ('full_name', 'email')
    list_filter = ('role',)