from django.contrib import admin
from .models import Resort, Booking
from django.contrib.auth.models import User 
#Registering my models
@admin.register(Resort)
class ResortAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_night', 'location')
    search_fields = ('name', 'location')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('resort', 'user', 'check_in_date', 'check_out_date')
    search_fields = ('resort__name', 'user__username')


