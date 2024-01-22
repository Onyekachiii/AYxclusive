from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import SiteVisitRequest, User, Profile, ContactUs, CustomFurnitureRequest


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Firstname'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lastname'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    house_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    phone = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Phone Number'}))
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
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image', 'bio', 'phone']
        
    
class ContactFormForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First name"})) 
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}))
    message = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'message'}))
    
    
    class Meta:
        model = ContactUs
        fields = ['first_name', 'last_name', 'phone', 'message']
        


class CustomFurnitureRequestForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}))
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Delivery Address"}))
    delivery_floor_level = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Delivery Floor Level"}))
    uploads = forms.ImageField(required=False, widget=forms.FileInput(attrs={"placeholder": "Uploads"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Furniture Type, Dimensions, Materials, etc.", "class": "custom-description-field"}))
        

class SiteVisitRequestForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    whatsapp_phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": " Whatsapp Phone"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Address"}))
    convenient_day_of_visit = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),input_formats=['%Y-%m-%d'])
    
    
    class Meta:
        model = SiteVisitRequest
        fields = ['first_name', 'last_name', 'email', 'whatsapp_phone', 'address', 'convenient_day_of_visit']
        widgets = {
            'convenient_day_of_visit': forms.DateInput(attrs={'type': 'date'}),
        }
        input_formats = ['%Y-%m-%d']