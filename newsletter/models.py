from django.db import models

# Create your models here.

class Subscribe(models.Model):
    email_id = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email_id