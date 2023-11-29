from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from core.forms import ProductReviewForm, ProjectImageForm
from core.models import Product, Category, ProductImages, ProductReview, Quotation, Invoice,Receipts, ProjectImage
from django.contrib.auth.decorators import login_required
from userauths.models import Profile, ContactUs
from userauths.forms import ProfileForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
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
        
    quotations = Quotation.objects.filter(user=request.user)
    invoices = Invoice.objects.filter(user=request.user)
    receipts = Receipts.objects.filter(user=request.user)
    
    context = {
        'form': form,
        'profile': profile,
        'quotations' : quotations,
        'invoices': invoices,
        'receipts': receipts,
        'image_form': image_form
        
        
    }
    return render (request, "core/dashboard.html", context)


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



def simple_mail(request):
    
    send_mail(subject='This is your subject', 
              message='This is your message', 
              from_email='django@mailtrap.club', 
              recipient_list=['test.mailtrap1234@gmail.com'],
              fail_silently=False
              )
    
    return HttpResponse('Message sent')


def message_mail(request):
    
    email= EmailMessage(subject='This is your subject', 
              message='This is your message', 
              from_email='django@mailtrap.club', 
              to=['test.mailtrap1234@gmail.com'],
              bcc = ['bcc@anotherbestuser.com'])
    
    email.send()
    
    return HttpResponse('Message sent')
    


def contact_us(request):
    return render(request, 'core/contact_us.html')

# For contact form
def ajax_contact_form(request):
    first_name = request.GET['first_name']
    last_name = request.GET['last_name']
    email = request.GET['email']
    phone_number = request.GET['phone_number']
    address = request.GET['address']
    floor_level = request.GET['floor_level']
    furniture_type = request.GET['furniture_type']
    description = request.GET['description']
    
    contact = ContactUs.objects.create(
        first_name = first_name,
        last_name = last_name,
        email = email,
        phone_number = phone_number,
        address = address,
        floor_level = floor_level,
        furniture_type = furniture_type,
        description = description
    )
    
    data = {
        "bool": True,
        "message": "Thank you for reaching out, we will contact you shortly."
    }
    return JsonResponse({"data":data})



def projects(request):
    images = ProjectImage.objects.all()
    return render(request, 'core/projects.html', {'images': images})
