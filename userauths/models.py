from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from django.core.mail import send_mail
from django.conf import settings


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=100, default="Firstname")
    last_name = models.CharField(max_length=100, default="Lastname")
    bio = models.CharField(max_length=100, blank=True, null=True)
    house_address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, default="+230 1234 5678")
    city = models.CharField(max_length=100, default="Port Louis")
    country = models.CharField(max_length=100, default="Mauritius")
    is_email_verified=models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", null=True, blank=True)
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True, default="+230 1234 5678")
    house_address = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True, default="Port Louis")
    country = models.CharField(max_length=500, null=True, blank=True, default="Mauritius")
    
    verified = models.BooleanField(default=False)
    
    
    
    def __str__(self):
            return self.user.first_name
    

def create_user_profile(sender, instance,created, **kwargs):
    if created: 
        Profile.objects.create(user=instance)
        
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class ContactUs(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(default="email@abc.com")
    address = models.CharField(max_length=500)
    floor_level = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    furniture_type = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class CustomFurnitureRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    delivery_address = models.TextField()
    delivery_floor_level = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    uploads = models.ImageField(upload_to="images", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.timestamp}"
    
    

