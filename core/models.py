from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User, Profile

# from django.contrib.auth.models import User


STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "★✩✩✩✩"),
    (2, "★★✩✩✩"),
    (3, "★★★✩✩"),
    (4, "★★★★✩"),
    (5, "★★★★★"),
)



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat_', alphabet="abcdefgh12345678")
    title = models.CharField(max_length=100, default="Category Title")
    image = models.ImageField(upload_to='category', blank=True, null=True, default="category.jpg")
    
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__ (self):
        return self.title
        

class Tags(models.Model):
    pass
        
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='prd_', alphabet="abcdefgh12345678")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    
    title = models.CharField(max_length=100, default="Product Title")
    image = models.ImageField(upload_to='product', blank=True, null=True, default="product.jpg")
    description = models.TextField(null=True, blank=True, default="This is the product")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99, null=True, blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=2.99, null=True, blank=True)
    specifications = models.TextField(null=True, blank=True, default="This is the product specifications")
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    
    product_status = models.CharField(choices=STATUS, max_length=20, default="in_review")
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=10, max_length=20, prefix='sku_', alphabet="abc12345678")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = 'Products'
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__ (self):
        return self.title
    
    # def get_percentage(self):
    #     new_price = (self.old_price - self.price) / self.old_price * 100
    #     return new_price
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.SET_NULL, null=True)
    images = models.ImageField(upload_to = "product-images", default="product.png")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"
        
        

####################################### Cart, Order, Items and Address ####################################
####################################### Cart, Order, Items and Address ####################################
####################################### Cart, Order, Items and Address ####################################
####################################### Cart, Order, Items and Address ####################################


class CartOrder(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99, null=True, blank=True)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    
    class Meta:
        verbose_name_plural = "Cart Order"
        

class CartOrderProducts(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=1.99, null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.image.url))
    
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' %(self.image))
    
    

###################################### Product Reviews, WishLists, Address ################################
###################################### Product Reviews, WishLists, Address ################################
###################################### Product Reviews, WishLists, Address ################################
###################################### Product Reviews, WishLists, Address ################################
###################################### Product Reviews, WishLists, Address ################################


class ProductReview(models.Model):
    user = models.ForeignKey( User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    rating = models.IntegerField(choices=RATING, default=None)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
        
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
    
class WishList(models.Model):
    user = models.ForeignKey( User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "WishLists"
    
    def __str__(self):
        return self.product.title
    
    
class Address(models.Model):
    user = models.ForeignKey( User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=150, null=True)
    mobile = models.CharField(max_length=150, null=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Address"
    
    
###################################### Quotations, Invoices, Receipts & Emails ################################
###################################### Quotations, Invoices, Receipts & Emails ################################
###################################### Quotations, Invoices, Receipts & Emails ################################
###################################### Quotations, Invoices, Receipts & Emails ################################
###################################### Quotations, Invoices, Receipts & Emails ################################
    
# For Quotations
class Quotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quotation_number = ShortUUIDField(unique=True, length=10, max_length=20, prefix='quo_', alphabet="abc12345678")
    file = models.FileField(upload_to='quotations/')
    quotation_date = models.DateTimeField(auto_now_add=True)
    email_subject = models.CharField(max_length=255)
    email_body = models.TextField()
    sent = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, choices=[
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('part_paid', 'Part-Paid'),
    ], default='unpaid')
    
    class Meta:
        verbose_name_plural = "Quotations"
    

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_number = ShortUUIDField(unique=True, length=10, max_length=20, prefix='inv_', alphabet="abc12345678")
    file = models.FileField(upload_to='invoices/')
    invoice_date = models.DateTimeField(auto_now_add=True)
    email_subject = models.CharField(max_length=255)
    email_body = models.TextField()
    sent = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, choices=[
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('part_paid', 'Part-Paid'),
    ], default='unpaid')
    
    class Meta:
        verbose_name_plural = "Invoices"


class Receipts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipt_number = ShortUUIDField(unique=True, length=10, max_length=20, prefix='rct_', alphabet="abc12345678")
    file = models.FileField(upload_to='receipts/')
    receipt_date = models.DateTimeField(auto_now_add=True)
    email_subject = models.CharField(max_length=255)
    email_body = models.TextField()
    sent = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, choices=[
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('part_paid', 'Part-Paid'),
    ], default='unpaid')
    
    class Meta:
        verbose_name_plural = "Receipts"


# For Emails
class EmailTemplate(models.Model):
    email_template = models.CharField(max_length=255, unique=True, default='default_template')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    attachment = models.FileField(upload_to='email_attachments/', blank=True, null=True)
     

    def __str__(self):
        return self.email_template
    
    

class ProjectImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')
    description = models.TextField()

    def __str__(self):
        return self.description


# For Wallet 


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
   

    def __str__(self):
        return f"{self.user.username}'s Wallet"



class WalletTransaction(models.Model):
    TRANSACTION_CHOICES = [
        ('addition', 'Addition'),
        ('deduction', 'Deduction'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.transaction_type} - {self.amount} - {self.timestamp}'




