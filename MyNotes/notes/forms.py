from django import forms 
from .models import Note 

class NotesForm(forms.ModelForm):   #A ModelForm is a Django form class that is automatically created based on a Model.It’s the base class. You use it to create your own form classes based on models.So NoteForm is a subclass of ModelForm. It’s your specific form for the Note model.
    class Meta:
        model=Note
        fields=['title','content']



# This is like saying:

# “Hey Django, please create a form for me based on the Note model, using just the title and content fields.”

# After that:
# Django automatically creates form fields for title and content.
# Django automatically applies validations (e.g., required fields, max_length).
# Django automatically connects .save() to the Note model.

# So We Create Just this minimal class:
# What Django creates behind the scenes:
# A fully functional form with:

# CharField input for title
# Textarea input for content
# All validations from the model
# The ability to create or update a Note object via .save()
# That’s why it’s called ModelForm — Django bridges your model to the form automatically.That’s the magic of ModelForm.




#User Signup form 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class signUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']