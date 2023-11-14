from django.contrib import admin
from core.models import Product, ProductImages, Category, CartOrder, CartOrderProducts, ProductReview, WishList, Address, Quotation
from .actions import send_quotation_email


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'featured', 'product_status', 'pid']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    
    
class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status']
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']
    
class CartOrderProductsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'review']

class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']
    
class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'status']
    
class QuotationAdmin(admin.ModelAdmin):
    actions = [send_quotation_email]

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Remove the default "delete_selected" action
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def send_email_button(self, obj):
        return f'<a class="button" href="?send_email={obj.id}">Send Email</a>'

    send_email_button.short_description = 'Send Email'
    send_email_button.allow_tags = True

    list_display = ('user', 'quotation_number', 'date', 'sent')

    

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderProducts, CartOrderProductsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Quotation, QuotationAdmin)
    