from django.db import models
from django.contrib.auth.models import User
from PIL import Image

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('buyer', 'Buyer'),
    ('requester', 'Requester'),
    ('vendor', 'Vendor'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='requester')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_buyer(self):
        return self.role == 'buyer'
    
    def is_requester(self):
        return self.role == 'requester'
    
    def is_vendor(self):
        return self.role == 'vendor'
