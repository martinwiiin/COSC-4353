from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'address1', 'city', 'state', 'zip_code']  

admin.site.register(Profile, ProfileAdmin)
