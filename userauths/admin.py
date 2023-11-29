from django.contrib import admin
from userauths.models import User, Profile, ContactUs


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'bio')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'phone', 'verified')
    
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'furniture_type')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
