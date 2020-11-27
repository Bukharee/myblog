from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    bio = models.CharField(max_length=200, )
    github = models.CharField(blank=True, max_length=50)
    facebook = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)

    def get_absolute_url(self):
        return reverse('account:update', args=[self.request.user])
