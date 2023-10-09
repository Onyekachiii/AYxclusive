from django.urls import path
from core.views import index, about_us


app_name = 'core'

urlpatterns = [
    # homepage
    path('', index, name='index'),
    
    # About us
    path('about-us/', about_us, name='about-us'),
]