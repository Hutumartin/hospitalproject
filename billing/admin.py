from django.contrib import admin
from .models import Billing

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'appointment', 'amount', 'status', 'created_at')
    search_fields = ('patient__full_name',)
    list_filter = ('status',)