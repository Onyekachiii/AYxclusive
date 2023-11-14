from django.urls import path
from core.views import index, about_us, category_list_view, product_list_view, product_detail_view, category_product_list_view, customer_dashboard


app_name = 'core'

urlpatterns = [
    # homepage
    path('', index, name='index'),
    
    # For Categories
    path('category/', category_list_view, name='category-list'),
    path('category/<cid>/', category_product_list_view, name='category-product-list'),
    
    # For products
    path('products/', product_list_view, name='product-list'),
    path('products/<pid>/', product_detail_view, name='product-detail'),
    
    # About us
    path('about-us/', about_us, name='about-us'),
    
    # Customer Dashboard
    path('dashboard/', customer_dashboard, name='dashboard'),
    

    

]