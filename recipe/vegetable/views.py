from django.shortcuts import render,redirect
from .models import Recipe
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required  #only when user login, he can see recipe page.

from django.contrib.auth.models import User   #for authentication purpose
# Create your views here.

#Sending data from frontend to backend and vice-versa.

@login_required(login_url="login")
def recipes(request):
    if request.method=="POST":
        data=request.POST
        recipe_name=data.get('recipe_name')
        recipe_description=data.get('recipe_description')
        # print(recipe_name)
        # print(recipe_description)

        recipe_image=request.FILES.get('recipe_image')   #request.FILES to send images to backend
        # print(recipe_image)

        Recipe.objects.create(                     #Pushing data from frontend to backend
            name=recipe_name,
            description=recipe_description,
            image=recipe_image,
        )
        return redirect('view_recipe')   #name of url
    
    queryset=Recipe.objects.all()   #Getting data fron backend to frontend

    if request.GET.get('search'):
        #print(request.GET.get('search'))
        queryset=queryset.filter(name__icontains=request.GET.get('search'))  #Recipe name ke andar jo bhi hamne search kiya hai usmese kuch key ati hai ki nahi
        
    
    context={'recipes':queryset}

    return render(request,'recipes.html',context)


#Delete

@login_required(login_url="login")
def delete_recipe(request,id):
    queryset=Recipe.objects.get(id=id)
    queryset.delete()

    return redirect('view_recipe')


#Update

@login_required(login_url="login")
def update_recipe(request,id):
    queryset=Recipe.objects.get(id=id)
    if request.method=="POST":
        data=request.POST

        name=data.get('recipe_name')                  #must be same as the name defined in html file there
        description=data.get('recipe_description')
        image=request.FILES.get('recipe_image')

        queryset.name=name
        queryset.description=description

        if image:
            queryset.image=image

        queryset.save()

        return redirect('view_recipe')
    
    context={'recipe':queryset}

    return render(request,'update_recipe.html',context)


def login_page(request):
    return render(request,'login.html')


def register(request):
    if request.method=="POST":
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username= request.POST.get('username')
        password= request.POST.get('password')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already exists!!!")
            return  redirect('reg_page')
        
        user= User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
            #password=password, we will not get encrypted pw by this way,it considers it as a regular string.
        )
        user.set_password(password)   #By default,we have this method in django's User model to get encrypted pw.
        user.save()  
        messages.info(request, 'Account created Successfully.')                 #When you enter a password in an HTML form, the password is sent as plain text from the browser to the server.Django provides the set_password method, which is used to hash the password before storing it in the database. This ensures that even if someone gains access to your database, they won't be able to read the passwords.

        return redirect('reg_page')

    return render(request,'register.html')





def login_page(request):
    if request.method=="POST":
        username= request.POST.get('username')
        password= request.POST.get('password')

        if not User.objects.filter(username=username).exists():     #if username not exists
            messages.error(request,'Invalid Username.')
            return redirect('login_page')
        
        user = authenticate(username = username, password = password) #If username is valid then  check if pw is correct for that username or not.Will return None if pw does not match.
        
        if user is None:
            messages.error(request,'Invalid Password.')
            return redirect('login_page')
        else:
            login(request,user)  
            return redirect('view_recipe') 

    return render(request,'login.html')                                                   #else put it into session so that browser saves it automatically hence when next time user will come,he don't need to login again until session do not get expired.For that in django there is login method which maintains session.



def logout_page(request):
    logout(request)        #request vale session me sab chije mil jayengi vahase remove kar denga
    return redirect('login_page')



