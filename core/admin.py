from django.contrib import admin
from core.models import CartOrderRequest, Comment, OutstandingPayment, PrivacyPolicy, Product, ProductImages, Category, CartOrder, CartOrderProducts, RefundPolicy, ReturnsAndCancellations, TermsAndConditions, WalletUsage, WarrantyPolicy, WishList, Address, Quotation, Invoice, Receipts, ProjectImage, Wallet, WalletTransaction, BalanceStatement, Document, WalletFundsTransfer
# from .utils import send_custom_email
from django import forms
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.utils.html import format_html, mark_safe
from decimal import Decimal





class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'featured', 'product_status', 'pid']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    
    

    
class CartOrderProductsInline(admin.TabularInline):
    model = CartOrderProducts
    extra = 1
    list_display = ['cart_invoice_no', 'item', 'image', 'qty', 'price', 'total']
    

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date']
    inlines = [CartOrderProductsInline]
    
    
class CartOrderRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'phone', 'delivery_address', 'delivery_floor_level', 'description']


class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']
    
class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'status']
    

class QuotationAdmin(admin.ModelAdmin):
    
    list_display = ['user', 'quotation_number', 'is_approved', 'wallet_usage', 'quotation_date']

    def is_approved(self, obj):
        return obj.approved  # Assuming your Quotation model has an 'approved' field
    is_approved.boolean = True
    is_approved.short_description = 'Approved'
    
class OutstandingPaymentAdmin(admin.ModelAdmin):
    list_display =['user', 'payment_amount', 'timestamp', 'proof_of_payment']
    fields = ['user', 'payment_amount', 'proof_of_payment']
    
    
class WalletFundsTransferAdmin(admin.ModelAdmin):
    list_display =['user', 'funds_amount', 'timestamp', 'proof_of_transfer']
    fields = ['user', 'funds_amount', 'proof_of_transfer']

    

class WalletUsageAdmin(admin.ModelAdmin):
    list_display = ['user', 'quotation', 'amount_used']


class InvoiceAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'invoice_number', 'amount_to_be_paid', 'payment_status', 'proof_of_invoice_display', 'invoice_date')
    
    def proof_of_invoice_display(self, obj):
        if obj.proof_of_invoice:
            return mark_safe('<a href="{0}" target="_blank">View Proof of Invoice</a>'.format(obj.proof_of_invoice.url))
        return 'No proof of invoice'

    proof_of_invoice_display.short_description = 'Proof of Invoice'


class DocumentAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'document_number')
    
    
class ReceiptAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'receipt_number')
    

class CommentInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Comment
    extra = 1

class ProjectImageAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('user', 'description', 'is_approved')  # Include is_approved in the list display
    actions = ['approve_images']

    def approve_images(self, request, queryset):
        queryset.update(is_approved=True)
    approve_images.short_description = "Approve selected images"
    

class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']
    actions = None

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<str:wallet_id>/add_to_balance/', self.add_to_balance, name='add_to_balance'),
            path('<str:wallet_id>/subtract_from_balance/', self.subtract_from_balance, name='subtract_from_balance'),
        ]
        return custom_urls + urls

    
    def add_to_balance(self, request, wallet_id):
        wallet = Wallet.objects.get(pk=wallet_id)
        if request.method == 'POST':
            amount_to_add = Decimal(request.POST['amount'])
            description = request.POST['description']  # Get the description from the form
            wallet.balance += amount_to_add
            wallet.save()

            WalletTransaction.objects.create(
                user=wallet.user,
                transaction_type='addition',
                amount=amount_to_add,
                description=description  # Save the description in the WalletTransaction model
            )
            return redirect('admin:core_wallet_changelist')
        return render(request, 'admin/add_to_balance.html', {'wallet': wallet})

    def subtract_from_balance(self, request, wallet_id):
        wallet = Wallet.objects.get(pk=wallet_id)
        if request.method == 'POST':
            amount_to_deduct = Decimal(request.POST['amount'])
            description = request.POST['description']  # Get the description from the form
            wallet.balance -= amount_to_deduct
            wallet.save()

            WalletTransaction.objects.create(
                user=wallet.user,
                transaction_type='deduction',
                amount=amount_to_deduct,
                description=description  # Save the description in the WalletTransaction model
            )
            return redirect('admin:core_wallet_changelist')
        return render(request, 'admin/subtract_from_balance.html', {'wallet': wallet})

    def add_to_balance_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Add</a>',
            reverse('admin:add_to_balance', args=[obj.pk])
        )
    add_to_balance_button.short_description = 'Add to Balance'

    def subtract_from_balance_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Deduct</a>',
            reverse('admin:subtract_from_balance', args=[obj.pk])
        )
    subtract_from_balance_button.short_description = 'Deduct from Balance'

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if 'add_to_balance_button' not in list_display:
            list_display.append('add_to_balance_button')
        if 'subtract_from_balance_button' not in list_display:
            list_display.append('subtract_from_balance_button')
        return list_display
    


class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'timestamp', 'get_description']

    def get_description(self, obj):
        # Assuming you have a description field in your WalletTransaction model
        return obj.description

    get_description.short_description = 'Description'


class BalanceStatementAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'description', 'invoice_no', 'invoice_amount', 'paid_amount', 'balance_amount']



admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletUsage, WalletUsageAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
admin.site.register(WalletFundsTransfer, WalletFundsTransferAdmin)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)

admin.site.register(CartOrderRequest, CartOrderRequestAdmin)
admin.site.register(Comment)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Quotation, QuotationAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Receipts, ReceiptAdmin)
admin.site.register(ProjectImage)
admin.site.register(BalanceStatement, BalanceStatementAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(OutstandingPayment, OutstandingPaymentAdmin)
admin.site.register(TermsAndConditions)
admin.site.register(RefundPolicy)
admin.site.register(WarrantyPolicy)
admin.site.register(ReturnsAndCancellations)
admin.site.register(PrivacyPolicy)

    