from django.urls import path
from userauths import views

from django.contrib.auth import views as auth_views
# auth_views.PasswordResetView.as_view
# auth_views.PasswordResetDoneView.as_view
# auth_views.PasswordResetConfirmView.as_view
# auth_views.PasswordResetCompleteView.as_view

app_name = 'userauths'

urlpatterns = [
    path('sign-up', views.register_view, name='sign-up'),
    path('sign-in', views.login_view, name='sign-in'),
    path("sign-out/", views.logout_view, name="sign-out"),
    
    # For Contact Us page
    path('contact/', views.contact_us, name='contact'),
    
    
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    




  
    
    
]