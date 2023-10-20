from core.models import Product, ProductImages, Category
from django.contrib import messages


def default(request):
    categories = Category.objects.all()
    
        
    
    return{
        'categories': categories,
    }