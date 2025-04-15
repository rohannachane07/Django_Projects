from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from .forms import signUpForm

# Create your views here.
from .models import Note
from .forms import NotesForm

@login_required
def home(request):
    notes=Note.objects.filter(user=request.user).order_by('created_at')   #Note.objects.all() fetches all Note objects from the database.sorts notes with latest first.   Then we modiefied it for specific user.Now it Shows only the notes created by the currently logged-in user.
    return render(request, 'home.html',{'notes':notes})  #renders the home.html template and sends the list of notes to it using a dictionary


def add_note(request):
    if(request.method=='POST'):  #checks if the form is submitted.
        form=NotesForm(request.POST)  # loads data from the form into the form object.
        if form.is_valid():  #Django automatically validates required fields.
            note=form.save(commit=False)    #previously form.save() was there which saves the new note to the database. Now we will modify code for authentication.  That note variable is just a temporary Python variable holding the form data — it has nothing to do with the model name itself.
            note.user=request.user
            note.save()        
            return redirect('home')   # after saving, redirects to home.
    else:
        form=NotesForm()  #if not submitted, show an empty form.
    return render(request,'add_note.html',{'form':form})  #passes the form to add_note.html.




def edit_note(request,note_id):  #note_id is received from the URL (edit/3/, for example).
    note=get_object_or_404(Note,id=note_id)   #tries to fetch the note. If it doesn’t exist, it shows a 404 error.id  comes from Django’s model system.
   #When you define a model in models.py, Django automatically creates a primary key field called id(an auto-incrementing integer).
    if request.method=="POST" :
        form=NotesForm(request.POST, instance=note)  # loads the form with existing data of that specific note.instance is an argument to the ModelForm(Means actually it's an argument to the form class we're creating (NotesForm), which inherits from Django’s ModelForm).
       # It is used when you want the form to work with an existing database object.If you pass instance=note, it will update the note.If you don’t pass instance, it will create a new note.
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=NotesForm(instance=note)  #If it's a GET request (user is visiting the edit page), show the form pre-filled with the existing note data.


    return render(request,'edit_note.html',{'form':form})

def delete_note(request,note_id):
    note=get_object_or_404(Note,id=note_id)
    if request.method=='POST':
        note.delete()
        return redirect('home')
    return render(request,'delete.html',{'note':note})

def signup_view(request):
    if(request.method=='POST'):
        form=signUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)  #Auto-login after signup
            return redirect('home')
        
    else:
        form=signUpForm()
    return render(request,'signup.html',{'form':form})
#Django already provides login and logout views you can use directly. Just set them up in your urls.py.








# form = NoteForm(instance=note)
# When you write that, you're doing exactly this:

# You are instantiating (creating an object of) the class NoteForm.
# That means Python calls the __init__() method inside the ModelForm class, which NoteForm inherits from.

# So even though you don't see it, Django’s ModelForm has an __init__() constructor like this:
# def __init__(self, *args, **kwargs):
#     instance = kwargs.get('instance')
#     # set up form fields, bind data, etc.

# So what is happening here:
# You're calling the constructor of the NoteForm class.
# Under the hood, Django uses the constructor (__init__) from the ModelForm base class.
# That constructor receives your instance keyword argument.
# Django uses it to pre-fill the form fields with that instance’s data.




# note_id is NOT automatically created by Django.
# We are the one who passes it in the URL .
# The user clicks edit, which links to /edit/3/
# Django passes note_id=3 into the view.
# We use get_object_or_404() to safely fetch that note from the database using the id.

# get_object_or_404(ModelName, field_name=value)
# In our case:
# ModelName = Note
# field_name = id
# value = note_id (passed from URL)
# So Django interprets:
# Note.objects.get(id=note_id)
# Which means:
# “Get the Note object whose id matches the note_id.”



#-----------------------------------------------------------------------------------------------------
# 1. note = form.save(commit=False)
# form.save() usually saves the form directly to the database.
# But when you do commit=False, it creates a Note object from the form, but does NOT save it yet.

# Why?
# So you can add or change something (like attaching the logged-in user) before saving.

# 🧠 Think of it like:
# “Hey Django, get my form data ready as a Note object, but hold off on saving it to the DB.”

# ✅ 2. note.user = request.user
# Here, you're assigning the currently logged-in user (request.user) to the user field of the note.
# This connects the note to the correct user.

# 🧠 Remember:
# Your Note model has this line:

# user = models.ForeignKey(User, on_delete=models.CASCADE)
# So you must assign a user before saving!

# ✅ 3. note.save()
# Now that everything is ready (title, content, and user), you save it to the database.
# This executes the SQL INSERT and stores the note.








 





    









