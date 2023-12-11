from django.contrib import admin
from userauths.models import User, Profile, ContactUs, CustomFurnitureRequest


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'phone', 'verified')
    
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
    

class CustomFurnitureRequestAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'delivery_address', 'delivery_floor_level', 'timestamp']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'delivery_address', 'delivery_floor_level']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(CustomFurnitureRequest, CustomFurnitureRequestAdmin)
