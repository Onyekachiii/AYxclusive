from django.shortcuts import render, redirect, get_object_or_404
from core.forms import ProductReviewForm
from core.models import Product, Category, ProductImages, ProductReview, Quotation
from django.contrib.auth.decorators import login_required
from userauths.models import Profile
from userauths.forms import ProfileForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage



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

@login_required
def customer_dashboard(request):
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
        
    quotations = Quotation.objects.filter(user=request.user)
    
    context = {
        'form': form,
        'profile': profile,
        'quotations' : quotations,
        
    }
    return render (request, "core/dashboard.html", context)



def simple_mail(request):
    
    send_mail(subject='This is your subject', 
              message='This is your message', 
              from_email='django@mailtrap.club', 
              recipient_list=['test.mailtrap1234@gmail.com'])
    
    return HttpResponse('Message sent')


def message_mail(request):
    
    email= EmailMessage(subject='This is your subject', 
              message='This is your message', 
              from_email='django@mailtrap.club', 
              to=['test.mailtrap1234@gmail.com'],
              bcc = ['bcc@anotherbestuser.com'])
    
    email.send()
    
    return HttpResponse('Message sent')
    


