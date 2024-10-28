from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(blank=True,upload_to='profile-pics')

    def __str__(self) -> str:
        return self.user.username