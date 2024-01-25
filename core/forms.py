from django import forms
from userauths.models import ContactUs
from core.models import BalanceStatement, CartOrderRequest, Comment, Invoice, WalletUsage

from core.models import ProductReview, ProjectImage, Document



class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'Placeholder': "Write review"}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        
        

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'description', 'is_approved']
        

class WalletUsageForm(forms.ModelForm):
    class Meta:
        model = WalletUsage
        fields = ['amount_used']
        

class BalanceStatementForm(forms.ModelForm):
    class Meta:
        model = BalanceStatement
        fields = '__all__'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['description', 'document_number', 'file']
        
        
class CartOrderRequestForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}))
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Delivery Address"}))
    delivery_floor_level = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Delivery Floor Level"}))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Description"}))
    
    
    class Meta:
        model = CartOrderRequest
        fields = ['first_name', 'last_name', 'email', 'phone', 'delivery_address', 'delivery_floor_level', 'description']


class CommentForm(forms.ModelForm):
    image_id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Comment
        fields = ['text']


class PaymentConfirmationForm(forms.Form):
    proof_of_invoice = forms.FileField(label='Proof of Payment', required=True)
    
