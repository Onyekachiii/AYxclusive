from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile, ContactUs


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Firstname'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lastname'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    house_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    phone = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
    floorlevel = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Delivery Floor Level'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    
    
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
        
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First name"})) 
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lastname'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"placeholder": "Image"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}))
    house_address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Address"}))
    floorlevel = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Delivery Floor Level'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image', 'bio', 'phone']
        
    
class ContactFormForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First name"})) 
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Address"}))
    floor_level = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Delivery Floor Level'}))
    furniture_type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Furniture type'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Description'}))
    
    
    class Meta:
        model = ContactUs
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'floor_level', 'furniture_type', 'description']