from django.db import models

# Create your models here.

class Message(models.Model):
    text = models.TextField()
    response = models.TextField()

    def __str__(self):
        return self.text
