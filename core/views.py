from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from core.forms import ProductReviewForm, ProjectImageForm
from core.models import Product, Category, ProductImages, ProductReview, Quotation, Invoice,Receipts, ProjectImage, Wallet, WalletTransaction, BalanceStatement, Document, WishList, CartOrder, CartOrderProducts
from django.contrib.auth.decorators import login_required
from userauths.models import Profile, ContactUs
from userauths.forms import ProfileForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
from django.core import serializers
from django.db.models import Count, Avg


# For sending mails
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.core.mail.message import EmailMessage
from django.utils.html import strip_tags




def index(request):
    products = Product.objects.filter(product_status= "published", featured=True)
    
    context = {
        "products": products,
    }
    return render(request, 'core/index.html', context)

# For about us page
def about_us(request):
    return render(request, 'core/about_us.html')


# To list products in shop
def product_list_view(request):
    products = Product.objects.filter(product_status= "published")
   
    
    context = {
        "products": products,

    }
    return render(request, 'core/product-list.html', context)
    

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, 'core/category-list.html', context)


# To list productzs in each category
def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status= "published", category=category)
    
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "core/category-product-list.html", context)


# To get a product detail
def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    product_images = ProductImages.objects.filter(product=product)
    # product_reviews = ProductReview.objects.filter(product=product)
    products = Product.objects.filter(product_status= "published", category=product.category).exclude(pid=pid)[:4]
    
    #To get all reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    #Product review form
    review_form = ProductReviewForm()
    
    make_review = True
    
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        
        if user_review_count == 1:
            make_review = False
    
    product_images = product.product_images.all()
    
    context = {
        "p": product,
        "make_review": make_review,
        "review_form": review_form,
        "product_images": product_images,
        "reviews": reviews,
        "products": products,
    }
    return render(request, 'core/product-detail.html', context)


# To search for products
def search_view(request):
    query = request.GET.get('q')
    
    if query is not None:
        products = Product.objects.filter(title__icontains=query).order_by('-date')
    
    
        context = {
            "query": query,
            "products": products,
        }
        return render(request, 'core/search.html', context)
    else:
        return render(request, 'core/search.html')   


# To filter products by categories & vendors
def filter_product(request):
    categories = request.GET.getlist('category[]')
    
    products = Product.objects.filter(product_status= "published").order_by("-id").distinct()
    
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
    
        
    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data":data})




@login_required
def customer_dashboard(request):
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                new_profile = form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
                messages.success(request, "Profile updated successfully")
                return redirect("core:dashboard")
        
        else:
            form = ProfileForm(instance=profile)
    
        
    
        image_form = ProjectImageForm()
        if request.method == 'POST':
            form = ProjectImageForm(request.POST, request.FILES)
            if form.is_valid():
                image_instance = form.save(commit=False)
                image_instance.user = request.user
                image_instance.save()
                return redirect('core:projects')
            
        current_user = request.user
        user_wallet = Wallet.objects.get(user=request.user)
        
        transactions = WalletTransaction.objects.filter(user=current_user).order_by('-timestamp')
        statements = BalanceStatement.objects.filter(user=current_user).order_by('-date')
        documents = Document.objects.filter(user=current_user)
        
  
        quotations = Quotation.objects.filter(user=request.user)
        invoices = Invoice.objects.filter(user=request.user)
        receipts = Receipts.objects.filter(user=request.user)
    
        context = {
            'user': current_user,
            'form': form,
            'profile': profile,
            'quotations' : quotations,
            'invoices': invoices,
            'receipts': receipts,
            'image_form': image_form,
            'user_wallet': user_wallet,
            'transactions': transactions,
            'statements': statements,
            'documents': documents
        
        
        }
        return render (request, "core/dashboard.html", context)
    
    else:
        return redirect('core:index')
    
def display_payment_details(request, invoice_id):
    print("Invoice ID:", invoice_id)
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    print("Invoice Data:", invoice.__dict__)

    return render(request, 'core:dashboard.html', {'invoice': invoice})
    

def approve_quotation(request, quotation_id):
    try:
        quotation = Quotation.objects.get(id=quotation_id, user=request.user)
        

        if request.method == 'POST':
            # Perform the approval action
            quotation.is_approved = True
            quotation.save()

            # Optionally, send a message to the Django admin
            messages.info(request, f"Quotation {quotation.quotation_number} has been approved.")

            # Send email to admin
            subject = 'Quotation Approved'
            user_name = request.user.get_full_name()  # Assuming your User model has a get_full_name method
            message = render_to_string('email/admin_notification_email.html', {'quotation': quotation, 'user_name': user_name})
            plain_message = strip_tags(message)  # Strip HTML tags for a plain text version
            from_email = 'testingexclusive123@gmail.com'  # Use your own email here
            to_email = 'stanleyonyekachiii@yahoo.com'  # Use your admin's email here

            send_mail(subject, plain_message, from_email, [to_email], html_message=message)

        # Redirect or return a response
        return redirect('core:dashboard')

    except Quotation.DoesNotExist:
        return HttpResponse("Quotation not found or you don't have permission to approve it.")


@login_required
def upload_image(request):
    if request.method == 'POST':
        image_form = ProjectImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image_instance = image_form.save(commit=False)
            image_instance.user = request.user
            image_instance.save()
            return redirect('core:projects')
    else:
        image_form = ProjectImageForm()

    return render(request, 'upload_image.html', {'image_form': image_form})   




def projects(request):
    images = ProjectImage.objects.all()
    return render(request, 'core/projects.html', {'images': images})



# To add to wishlist
def add_to_wishlist(request):
    id = request.GET['id']
    product = Product.objects.get(id=id)
    
    context = {}
    
    wishlist_count = WishList.objects.filter(user=request.user, product=product).count()
    print(wishlist_count)
    
    if wishlist_count > 0:
        context = {
            "bool": True,
        }
    else:
        new_wishlist = WishList.objects.create(
            product = product,
            user = request.user
        )
        context ={
            "bool": True,
        }
    
    return JsonResponse(context)

# To view wishlist
@login_required
def wishlist_view(request):
    wishlist = WishList.objects.filter(user=request.user)

    context = {
        "w" : wishlist,
    }
    return render(request, "core/wishlist.html", context)


# To remove from wishlist
@login_required
def remove_from_wishlist(request):
    pid = request.GET['id']
    wishlist = WishList.objects.filter(user=request.user)
    product = WishList.objects.get(id=pid)
    product.delete()
    
    context = {
        "bool" : True,
        "w": wishlist,
    }
    wishlist_json = serializers.serialize('json', wishlist)
    data = render_to_string("core/async/wishlist-list.html", context)
    return JsonResponse({"data": data, "w": wishlist_json})


# To add to cart
def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'price': request.GET['price'],
        'qty':  request.GET['qty'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    
    else:
        request.session['cart_data_obj'] = cart_product
        
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


# To list products in cart
@login_required
def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                cart_total_amount += int(item['qty']) * float(item['price'])
            except ValueError:
            # Handle the case where item['price'] is not a valid float
                pass
        return render(request, 'core/cart.html', {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect('core:index')
    
    
# To delete item from cart
@login_required
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) 
    
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})


# To update cart
@login_required
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = int(request.GET['qty'])
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) 
    
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})


def warranty_policy(request):
    return render(request, 'core/warranty-policy.html')

def refund_policy(request):
    return render(request, 'core/refund-policy.html')

def returns_and_cancellations(request):
    return render(request, 'core/returns-and-cancellations.html')

def privacy_policy(request):
    return render(request, 'core/privacy-policy.html')

def terms_and_conditions(request):
    return render(request, 'core/terms-and-conditions.html')

def faq_view(request):
    return render(request, 'core/FAQ.html')


def confirm_payment(request, invoice_id):


    try:
        invoice = Invoice.objects.get(id=invoice_id, user=request.user)
        

        if request.method == 'POST':
            

            # Optionally, send a message to the Django admin
            messages.info(request, f"Invoice {invoice.invoice_number} has been approved.")

            # Send email to admin
            subject = 'Invoice Payment made'
            user_name = request.user.get_full_name()  # Assuming your User model has a get_full_name method
            message = render_to_string('email/payment_made_admin_notification.txt', {'invoice': invoice, 'user_name': user_name})
            plain_message = strip_tags(message)  # Strip HTML tags for a plain text version
            from_email = 'testingexclusive123@gmail.com'  # Use your own email here
            to_email = 'stanleyonyekachiii@yahoo.com'  # Use your admin's email here

            send_mail(subject, plain_message, from_email, [to_email], html_message=message)

        # Redirect or return a response
        return redirect('core:dashboard')

    except Invoice.DoesNotExist:
        return HttpResponse("Invoice not found or you don't have permission to pay for it.")