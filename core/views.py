from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from core.forms import CartOrderRequestForm, CommentForm, PaymentConfirmationForm, ProductReviewForm, ProjectImageForm, WalletUsageForm
from core.models import Comment, OutstandingPayment, PrivacyPolicy, Product, Category, ProductImages, ProductReview, Quotation, Invoice,Receipts, ProjectImage, RefundPolicy, ReturnsAndCancellations, TermsAndConditions, Wallet, WalletFundsTransfer, WalletTransaction, BalanceStatement, Document, WalletUsage, WarrantyPolicy, WishList, CartOrder, CartOrderProducts
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
                # Set is_approved to False by default
                image_instance.is_approved = False
                image_instance.save()
                return redirect('core:projects')
            
        current_user = request.user
        user_wallet = Wallet.objects.get(user=request.user)
        
        transactions = WalletTransaction.objects.filter(user=current_user).order_by('-timestamp')
        statements = BalanceStatement.objects.filter(user=current_user).order_by('-date')
        overall_balance = current_user.get_user_balance()
        documents = Document.objects.filter(user=current_user)
        
  
        quotations = Quotation.objects.filter(user=request.user)
        # invoice_id = request.GET.get('invoice_id')
        invoices = Invoice.objects.filter(user=request.user)
        payment_confirmation_form = PaymentConfirmationForm()
        receipts = Receipts.objects.filter(user=request.user)
        
        # invoice = None
        # if invoices.exists():
        
        invoice = Invoice.objects.filter(user=request.user, payment_status='unpaid').first()

        
    
        context = {
            'user': current_user,
            'form': form,
            'profile': profile,
            'quotations' : quotations,
            'quotation': None,
            'invoice': invoice,
            'invoices': invoices,
            # 'invoice_id': invoice_id,
            'receipts': receipts,
            'image_form': image_form,
            'user_wallet': user_wallet,
            'transactions': transactions,
            'statements': statements,
            'overall_balance': overall_balance,
            'documents': documents,
            'payment_confirmation_form': payment_confirmation_form,  
        
        }
        
        quotation_id = request.GET.get('quotation_id')

        # Move this block after defining 'quotation_id'
        quotation_id = request.GET.get('quotation_id')
        print("quotation_id:", quotation_id)  # Debugging line
        if quotation_id:
            try:
                quotation = Quotation.objects.get(id=quotation_id, user=request.user)
                context['quotation'] = quotation
            except Quotation.DoesNotExist:
                # Handle the case where the quotation doesn't exist
                pass
        
        print("context:", context)  # Debugging line
        
        return render (request, "core/dashboard.html", context)
    
    else: 
        return redirect('core:index')
    
    
def invoice_details(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    data = {
        'invoice_number': invoice.invoice_number,
        'invoice_date': str(invoice.invoice_date),
        'account_name': invoice.account_name,
        'account_number': invoice.account_number,
        'amount_to_be_paid': invoice.amount_to_be_paid,
        
    }
    return JsonResponse(data)


def payment_confirmation(request, invoice_id):
    
    try:
        invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)

        if request.method == 'POST':
            payment_confirmation_form = PaymentConfirmationForm(request.POST, request.FILES)
            
            
            if payment_confirmation_form.is_valid():
                # Save proof of invoice file to the invoice
                invoice.proof_of_invoice = payment_confirmation_form.cleaned_data['proof_of_invoice']
                invoice.save()

                # Optionally, send a message to the Django admin
                messages.info(request, f"Invoice {invoice.invoice_number} has been approved.")

                # Send email to admin
                subject = 'Invoice Payment made'
                user_name = request.user.get_full_name()
                message = render_to_string('email/payment_made_admin_notification.txt', {'invoice': invoice, 'user_name': user_name})
                plain_message = strip_tags(message)
                from_email = 'ayexclsv@gmail.com'  # Use your own email here
                to_email = 'ay.exclusive@outlook.com'  # Use your admin's email here

                send_mail(subject, plain_message, from_email, [to_email], html_message=message)

                

                # Render the payment confirmation page
                return render(request, 'core/payment-confirmation.html', {'invoice': invoice, 'payment_confirmation_form': payment_confirmation_form})
                
            else:
                messages.error(request, "Invalid form submission.")
        else:
            form = PaymentConfirmationForm()

        # Render the payment confirmation page
        return redirect('core:dashboard')

    except Invoice.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invoice not found or you do not have permission to pay for it.'})


def get_wallet_balance(request):
    if request.user.is_authenticated:
        user_wallet = Wallet.objects.get(user=request.user)
        balance = user_wallet.balance
        return JsonResponse({'balance': balance})
    else:
        return JsonResponse({'error': 'User not authenticated'})
    

def add_funds(request):
    if request.method == 'POST':
        
        # Process the form data
        funds_amount = request.POST.get('payment_amount')
        proof_of_transfer = request.FILES.get('proof_of_transfer')
        
        # Save the details in Django admin or your database model
        wallet_funds_transfer = WalletFundsTransfer.objects.create(
            user=request.user,
            funds_amount=funds_amount,
            proof_of_transfer=proof_of_transfer
        )
        wallet_funds_transfer.save()
        
        # Send email to admin
        subject = 'New Wallet Funds transfer'
        user_name = request.user.get_full_name()
        message = render_to_string('email/wallet_funds_transfer.html', {'wallet_funds_transfer': wallet_funds_transfer, 'user_name': user_name})
        plain_message = strip_tags(message)
        from_email = 'ayexclsv@gmail.com'  # Use your own email here
        to_email = 'ay.exclusive@outlook.com'  # Use your admin's email here

        send_mail(subject, plain_message, from_email, [to_email], html_message=message)
        # Return a JSON response indicating success
        messages.success(request, 'We will confirm payment and get back to you!')
        return redirect('core:dashboard')  # Adjust the redirect URL as needed
    else:
        return redirect('core:dashboard')  # Redirect to dashboard if not a POST request
    

@login_required
def approve_quotation(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id, user=request.user)

    if not quotation.is_approved and quotation.user == request.user:
        if request.method == 'POST':
            wallet_usage_form = WalletUsageForm(request.POST)
            if wallet_usage_form.is_valid():
                
                amount_used = wallet_usage_form.cleaned_data['amount_used']
                user_wallet = Wallet.objects.get(user=request.user)

                if amount_used > user_wallet.balance:
                    messages.error(request, "Amount to use cannot exceed wallet balance")
                   
                
                quotation.wallet_usage = amount_used
                quotation.is_approved = True
                quotation.save()
                
                # Send email to admin
                subject = 'Quotation Approved'
                user_name = request.user.get_full_name()
                message = render_to_string('email/admin_notification_email.html', {'quotation': quotation, 'user_name': user_name})
                plain_message = strip_tags(message)
                from_email = 'ayexclsv@gmail.com '  # Use your own email here
                to_email = 'ay.exclusive@outlook.com'  # Use your admin's email here

                send_mail(subject, plain_message, from_email, [to_email], html_message=message)

                messages.info(request, f"Quotation {quotation.quotation_number} has been approved with wallet usage.")

                return redirect('core:dashboard')

        else:
            wallet_usage_form = WalletUsageForm()

        return render(request, 'core/dashboard.html', {'quotation': quotation, 'wallet_usage_form': wallet_usage_form})
    else:
        return HttpResponse("Quotation not found or you don't have permission to approve it.")




def quotation_details(request, quotation_id):
    try:
        quotation = get_object_or_404(Quotation, id=quotation_id)
        # Modify this based on your actual Quotation model structure
        data = {
            'quotation_id': quotation.id,
            'quotation_number': quotation.quotation_number,
            # Add other details as needed
        }
        return JsonResponse(data)
    except Quotation.DoesNotExist:
        return JsonResponse({'error': 'Quotation not found'}, status=404)
    

def submit_wallet_usage(request, quotation_id):
    # Retrieve the quotation object
    quotation = Quotation.objects.get(id=quotation_id)

    # Extract the amount used from the wallet from the POST data
    amount_used = request.POST.get('amount_used')

    # Create a WalletUsage object
    wallet_usage = WalletUsage.objects.create(
        user=request.user,
        quotation=quotation,
        amount_used=amount_used
    )

    # Optionally, perform additional actions here

    # Return a JSON response indicating success
    return JsonResponse({'success': True})


def submit_payment(request):
    if request.method == 'POST':
        # Retrieve form data
        payment_amount = request.POST.get('payment_amount')
        proof_of_payment = request.FILES.get('proof_of_payment')


        outstanding_payment = OutstandingPayment.objects.create(
            user=request.user,
            payment_amount=payment_amount,
            proof_of_payment=proof_of_payment
        )
        outstanding_payment.save()

        # Send email to admin
        subject = 'New Outstanding Payment Submission'
        user_name = request.user.get_full_name()
        message = render_to_string('email/outstanding_payment_email.html', {'outstanding_payment': outstanding_payment, 'user_name': user_name})
        plain_message = strip_tags(message)
        from_email = 'ayexclsv@gmail.com'  # Use your own email here
        to_email = 'ay.exclusive@outlook.com'  # Use your admin's email here

        send_mail(subject, plain_message, from_email, [to_email], html_message=message)

                

        messages.success(request, 'We will confirm payment and get back to you!')
        return redirect('core:dashboard')  # Adjust the redirect URL as needed
    else:
        return redirect('core:dashboard')  # Redirect to dashboard if not a POST request

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
    images = ProjectImage.objects.filter(is_approved=True)
    comments = Comment.objects.filter(image__in=images)

    image_comments = {image.id: [] for image in images}
    for comment in comments:
        image_comments[comment.image_id].append(comment) 

    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.image_id = request.POST.get('image_id')  # Retrieve 'image_id' from the form
            comment.save()

    return render(request, 'core/projects.html', {'images': images, 'comment_form': comment_form, 'image_comments': image_comments})



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
@login_required
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
def clean_price_string(price_string):
    return ''.join(char for char in price_string if char.isdigit() or char == '.')


@login_required
def cart_view(request):
    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            if item['qty'] and item['price']:
                # Clean the price string before conversion
                cleaned_price_string = clean_price_string(item['price'])

                try:
                    cart_total_amount += int(item['qty']) * float(cleaned_price_string)
                except ValueError:
                    messages.error(request, f"Invalid price format for item {p_id}. Please check your cart.")
                    return redirect('core:index')

        return render(request, 'core/cart.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
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


# To checkout
@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0

    # Initializing the form variable
    form = CartOrderRequestForm()

    # Checking if cart_data_obj is in session
    cart_data_obj = request.session.get('cart_data_obj', None)
    
    if cart_data_obj is None:
        cart_data_obj = {} 
        
    if cart_data_obj:
        for product_id, item in cart_data_obj.items():
            total_amount += int(item['qty']) * float(item['price'])

        # Creating order objects
        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount,
        )

        # Getting total amount for the cart
        for product_id, item in cart_data_obj.items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_products = CartOrderProducts.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price']),
            )

        

    if request.method == 'POST':
        form = CartOrderRequestForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            

            # Send email to admin
            subject = 'New Order from Cart'
            user_name = request.user.get_full_name()  # Assuming your User model has a get_full_name method
            message = render_to_string('email/new_cart_order.html', {'order': order, 'user_name': user_name})
            plain_message = strip_tags(message)  # Strip HTML tags for a plain text version
            from_email = 'ayexclsv@gmail.com'  # Use your own email here
            to_email = 'ay.exclusive@outlook.com'  # Use your admin's email here

            send_mail(subject, plain_message, from_email, [to_email], html_message=message)
            
            # Clear the cart_data_obj from the session after processing
            del request.session['cart_data_obj']

            messages.success(request, 'Your cart order request has been submitted successfully.')
            return redirect('core/order-completed')
        
        


    else:
        # Get the user's profile
        user_profile = Profile.objects.get(user=request.user)

        # Prepopulate form fields with user profile data
        form_data = {
            'first_name': user_profile.user.first_name,
            'last_name': user_profile.user.last_name,
            'email': user_profile.user.email,
            'phone': user_profile.phone,  # Assuming phone is a field in your Profile model
        }

        # Update the form with the prepopulated data
        form = CartOrderRequestForm(initial=form_data)

    return render(request, 'core/checkout.html', {'cart_data': cart_data_obj,
                                                   'totalcartitems': len(cart_data_obj),
                                                   'cart_total_amount': cart_total_amount,
                                                   'form': form})


@login_required
def order_completed_view(request):
    
    return render(request, 'core/order-completed.html')



def warranty_policy(request):
    warranty_policy_content = WarrantyPolicy.objects.first()
    return render(request, 'core/warranty-policy.html', {'content': warranty_policy_content})

def refund_policy(request):
    refund_policy_content = RefundPolicy.objects.first()

    return render(request, 'core/refund-policy.html', {'content': refund_policy_content})

def returns_and_cancellations(request):
    returns_and_cancellations_content = ReturnsAndCancellations.objects.first()
    return render(request, 'core/returns-and-cancellations.html', {'content': returns_and_cancellations_content})

def privacy_policy(request):
    privacy_policy_content = PrivacyPolicy.objects.first()
    return render(request, 'core/privacy-policy.html', {'content': privacy_policy_content})

def terms_and_conditions(request):
    terms_and_conditions_content = TermsAndConditions.objects.first()

    return render(request, 'core/terms-and-conditions.html', {'content': terms_and_conditions_content})

def faq_view(request):
    return render(request, 'core/FAQ.html')
