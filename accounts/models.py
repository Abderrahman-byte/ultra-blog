from django.db import models
from django.contrib.auth.models import User

from PIL import Image
from blog.models import Tag

class Profil(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    profil_pic = models.ImageField(default='default.png')
    fav_tags = models.ManyToManyField(Tag)
    
    def save(self, *args, **kwargs) :
        super().save()

        img = Image.open(self.profil_pic.path)

        if str(img) != 'default.png' and (img.height > 300 or img.width > 300) :
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profil_pic.path)