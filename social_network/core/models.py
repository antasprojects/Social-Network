from django.db import models

# Create your models here.
class Profile(models.Model):
    user = pass
    id_user = pass
    bio = pass
    profileimg = models.ImageField(upload_to='profile_images', default=)
    location = pass

