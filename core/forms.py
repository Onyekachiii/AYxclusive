from django import forms
from userauths.models import ContactUs
from core.models import BalanceStatement

from core.models import ProductReview, ProjectImage, Document



class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'Placeholder': "Write review"}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        
        

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'description']
        


class BalanceStatementForm(forms.ModelForm):
    class Meta:
        model = BalanceStatement
        fields = '__all__'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['description', 'document_number', 'file']

