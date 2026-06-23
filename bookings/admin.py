from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_ref', 'customer', 'service', 'destination',
        'travel_date', 'status', 'created_at',
    )
    list_filter = ('status', 'service', 'budget_range')
    search_fields = ('booking_ref', 'customer__full_name', 'customer__email', 'destination')
    readonly_fields = ('booking_ref', 'created_at', 'updated_at')
