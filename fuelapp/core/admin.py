from django.contrib import admin
from .models import Profile, FuelQuote

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'address1', 'city', 'state', 'zip_code']  

admin.site.register(Profile, ProfileAdmin)

class FuelQuoteAdmin(admin.ModelAdmin):
    list_display = ['gallons_requested', 'delivery_address', 'delivery_date', 'suggested_price', 'total_amount_due']

admin.site.register(FuelQuote, FuelQuoteAdmin)

