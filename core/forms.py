from django import forms
from core.models import ProductReview, ProjectImage



class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'Placeholder': "Write review"}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        
        

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'description']

