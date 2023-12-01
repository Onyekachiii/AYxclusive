from django.contrib import admin
from core.models import Product, ProductImages, Category, CartOrder, CartOrderProducts, ProductReview, WishList, Address, Quotation, EmailTemplate, Invoice, Receipts, ProjectImage
# from .utils import send_custom_email
from django import forms




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
    

# class BaseAdmin(admin.ModelAdmin):
#     actions = ['send_email']

#     def send_email(self, request, queryset):
#         template_name = request.POST.get('email_template')
#         email_template = EmailTemplate.objects.get(template_name=template_name)

#         for obj in queryset:
#             context = {'object': obj, 'attachment': obj.attachment}
#             send_custom_email(obj.user_profile.user.email, email_template.subject, context=context)

#             obj.sent = True
#             obj.save()

#     send_email.short_description = 'Send selected objects via email'

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         # Remove any references to 'email_template' here if not present in the model
#         if 'email_template' in form.base_fields:
#             del form.base_fields['email_template']
#         return form



class QuotationAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'quotation_number', 'payment_status')



class InvoiceAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'invoice_number', 'payment_status')



class ReceiptAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'receipt_number', 'payment_status')
    

class ProjectImageAdmin (admin.ModelAdmin):
    list_display = ('user' )



admin.site.register(EmailTemplate)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderProducts, CartOrderProductsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Quotation, QuotationAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Receipts, ReceiptAdmin)
admin.site.register(ProjectImage)

    