from django.urls import path
from core.views import index, about_us, category_list_view, product_list_view, product_detail_view, category_product_list_view, customer_dashboard, search_view, filter_product, upload_image, projects


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
    
    # Search
    path('search/', search_view, name='search'),
    
    # Filter product URL
    path('filter-products/', filter_product, name='filter-product'),
    
    
    # path('ajax-contact-form/', ajax_contact_form, name='ajax-contact-form'),
    
    # To upload images from Forum page
    path('dashboard/upload/', upload_image, name='upload_image'),
    path('projects/', projects, name='projects'),


]