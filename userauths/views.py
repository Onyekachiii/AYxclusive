from audioop import reverse
from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm, ContactFormForm, CustomFurnitureRequestForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from verify_email.email_handler import send_verification_email
# from core.utils import send_custom_email
from userauths.models import ContactUs, Profile
from verify_email.email_handler import send_verification_email
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import account_activation_token

from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.http import HttpResponse


# For sending mails
from django.core.mail import send_mail
from django.core import mail
from django.core.mail.message import EmailMessage
from django.contrib.sites.shortcuts import get_current_site





User = settings.AUTH_USER_MODEL

    

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your AY Exclusive user account.'
    message = render_to_string('userauths/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email "{to_email}" inbox and click on \
            received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')




def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            
        
            return redirect("core:index")
        
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form
    }
    return render(request, "userauths/sign-up.html", context)



def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('userauths:sign-in')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('core:index')



def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
       
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")   
            return redirect("core:index")
            
        else:
            messages.warning(request, f"Invalid email and/or password, dont have an account? Create an account")        
    
    return render(request, "userauths/sign-in.html")
    

# To logout users
def logout_view(request):
    logout(request)
    messages.success(request, "You logged out successfully!")
    return redirect("userauths:sign-in")


def contact_us(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()

            
            messages.success(request, f"Thank you for contacting us, we will get back to you shortly!")   
            return redirect("core:index")
    else:
        form = ContactFormForm()

    return render(request, 'userauths/contact_us.html', {'form': form})

@login_required
def custom_furniture_request(request):
    
    if request.method == 'POST':
        form = CustomFurnitureRequestForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            
            messages.success(request, 'Your custom furniture request has been submitted successfully.')
            return redirect('core:dashboard')  # Change 'dashboard' to the appropriate URL
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

        # Create the form and pass the prepopulated data
        form = CustomFurnitureRequestForm(initial=form_data)

    return render(request, 'userauths/custom_furniture_request.html', {'form': form})



# def submit_custom_furniture_request(request):
#     if request.method == 'POST':
#         form = CustomFurnitureRequestForm(request.POST)
#         if form.is_valid():
#             # Handle form submission, e.g., send an email, save to the database, etc.
#             # Redirect to a thank-you page or the home page
#             form.save()
#             messages.success(request, f"Thank you for contacting us, we will get back to you shortly!")   
#             return redirect('core:index')
#     else:
#         form = CustomFurnitureRequestForm()

    # return render(request, 'userauths:custom_furniture_request', {'form': form})
