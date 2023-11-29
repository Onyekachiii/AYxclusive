from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from core.utils import send_custom_email




User = settings.AUTH_USER_MODEL

# To register users
def register_view(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            first_name= form.cleaned_data.get('first_name')
           
            send_custom_email(new_user.email, 'Welcome to AY Exclusive Furniture')
            messages.success(request, f'Hey {first_name}, your account has been created successfully!')
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password = form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('core:index')
        
        
    else:
        form = UserRegisterForm()
    
    
    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)


# To login users
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
            messages.success(request, f"Welcome {user.first_name}!")   
            return redirect("core:index")
            
        else:
            messages.warning(request, f"User with {email} does not exist, Create an account")
    
    return render(request, "userauths/sign-in.html")        
    

# To logout users
def logout_view(request):
    logout(request)
    messages.success(request, "You logged out successfully!")
    return redirect("userauths:sign-in")


