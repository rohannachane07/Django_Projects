# Create a Note model:
# title (CharField)
# content (TextField)
# created_at (DateTimeField, auto_now_add)

# Create a simple form to add a new note.

# Show a list of all saved notes on the homepage.

# No login required for now. Keep it simple.
#Add Edit & Delete Features to your Notes app.
#Then Level up and make your app multi-user — so that each user can create, view, edit, and delete only thei own notes. 
#Build User Login/Signup + User-specific Notes


from django.db import models

from django.contrib.auth.models import User  #Django comes with a ready-made User model:That model has these fields:username, password(encrypted), first_name, last_name, id(primary key)
# Create your models here.


class Note(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)     #We updated our Note model now to Link each Note to User.

    title=models.CharField(max_length=100)
    content=models.TextField(max_length=5000)
    created_at=models.DateTimeField(auto_now_add=True)  #set the field to the current date and time only once — when the object is created.It won’t change if you edit or update the note later.

    def __str__(self):
        return self.title
    


# You didn’t define id, so Django does this behind the scenes:
# id = models.AutoField(primary_key=True)
# When Django creates a model, the default id field is an AutoField. That means:
# Every time you save a new object to the database, Django assigns it the next available number in the sequence.

# Suppose You already created and deleted some notes earlier
# Maybe you added 2 notes while testing and then deleted them.
# AutoField does not reuse deleted IDs.
# So if you delete notes with id = 1 and 2, the next note will get id = 3.
# This is normal behavior in relational databases.

# Real-world mindset:
# Don’t worry about the number starting from 3, 100, or even 982.
# In real apps, the id is just a unique identifier — it doesn't need to be in perfect order.

#---------------------------------------------------------------------------------------------------------------------

# ✅ User → The Class (Model)
# This is the actual model that Django provides.
# You use it when defining relationships.Used in models.py, imports, queries.
# Here,user = models.ForeignKey(User, on_delete=models.CASCADE)-It represents the table where all users are stored.

# ✅ request.user → The Object (Instance of User)
# This is the specific user who's logged in — Django attaches it to each request.
# So basically:request.user is just one instance (row) of the User model, depending on who is logged in at that moment.

    

    

    

    



