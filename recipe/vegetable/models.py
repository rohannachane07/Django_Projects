from django.db import models

from django.contrib.auth.models import User   #The User model is defined in Django's authentication framework.It corresponds to the auth_user table in your db.sqlite3 database file.

class Recipe(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to="recipe")

    #user=models.ForeignKey(User,on_delete=models.CASCADE)      # If user gets deleted then all recipes related to him will also get deleted.
    #user=models.ForeignKey(User,on_delete=models.SET_DEFAULT)  # ....then set any default value to all recipes.
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)     #.... then set NULL to all recipes related to him.

    def __str__(self):
        return self.name


#ForeignKey- Using other table to get our work done.Using Key,we reference it,(here User).