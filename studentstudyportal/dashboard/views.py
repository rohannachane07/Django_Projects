#---------------------------------------------Notes---------------------------------------------
from django.shortcuts import render,redirect

from . models import *
from .forms import *
from django.contrib import messages
from django.views import generic

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method=="POST":
        form=NotesForm(request.POST)

        if form.is_valid():
            notes=Notes(user=request.user, title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request, f"Notes of {notes.title} Added By {request.user.username} Successfully!")  #To Display in frontend either we can do it in notes.html or base.html.
        return redirect('notes')
    
    else:
        form=NotesForm()  #Created a object
    
    notes=Notes.objects.filter(user=request.user) #user comes from Notes models which should be equal to request.user means our login user.                                          
    context={'notes':notes, 'form':form}
    return render(request,'dashboard/notes.html',context)
#Get all login user's notes and store it in object and pass using a context to our template file.


@login_required
def delete_note(request,pk=None):
    note =Notes.objects.get(id=pk)    #No need to store in note if we only want to delete and not want to show deleted message.
    title = note.title  # Save the title before deleting the only if we want to display the message of deletion.
    note.delete()
    messages.success(request, f"Notes of {title} deleted successfully!")
    return redirect('notes')



class notesDetailView(generic.DetailView):
    model=Notes
    
#This is a class-based view (CBV) for displaying the details of a single note. It uses Django's generic.DetailView and specifies Notes as the model. 
#This view automatically fetches the note object based on the pk provided in the URL and passes it to the template.
#The DetailView comes from Django's django.views.generic module, which contains various generic views designed to simplify common patterns in web development. 
#These generic views include ListView, CreateView, UpdateView, DeleteView, and others, each providing specific functionalities for different tasks.

# In Django, generic views are a set of built-in class-based views that provide common functionalities for common patterns of web development. These generic views handle many typical tasks 
# such as displaying a list of objects, creating a new object, updating an existing object, and deleting an object. They help reduce boilerplate code 
# and provide a clean and reusable way to build views.


#Inheritance: notesDetailView inherits from generic.DetailView. This means it automatically gains the functionality of a detail view, which includes fetching an object based on a primary key and rendering a template with the object's details.

#Model Specification: model = Notes specifies that this view will operate on the Notes model.

#Template Name: template_name = 'dashboard/notes_detail.html' specifies the template to use for rendering the details of the note. If not specified, Django will use a default naming pattern to find the template.

#URL Configuration: The URL pattern path('notes_detail/<int:pk>', views.notesDetailView.as_view(), name='notes-detail') maps to the notesDetailView class. The as_view() method is used to convert the class into a view function that can be called when the URL is accessed.
#Fetching the Object: When a request is made to the notes_detail/<int:pk> URL, the notesDetailView automatically fetches the Notes object with the primary key (pk) provided in the URL.
#Context Variable: The fetched Notes object is passed to the template as a context variable named object, but it can also be accessed using the model name in lowercase (notes in this case).
#Rendering the Template: The notes_detail.html template is rendered with the context data. The template can access the Notes object using the notes context variable.


#--------------------------------------------HomeWork----------------------------------------------------
@login_required
def homework(request):
    if request.method=="POST":
        form=HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':                  #The "on" keyword is not specific to Django but is a default behavior of HTML checkboxes in forms. When a checkbox is checked, its value is sent as "on" in the form submission. 
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            
            homeworks=Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request, f"Homework of Subject {homeworks.subject} Added By {request.user.username}!!")
    else:
        form=HomeworkForm()

    hw=Homework.objects.filter(user=request.user)
    # if len(hw)==0:
    #     homework_done=True
    # else:
    #     homework_done=False
    all_completed = all(hw_item.is_finished for hw_item in hw)  # Check if all homework items are completed

    context={'homework':hw, 'homeworks_done':all_completed,'form':form}
    return render(request, 'dashboard/homework.html',context)


@login_required
def update_homework(request, pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return redirect('homework')  #if a user refreshes the page after a form submission, the browser might resubmit the form data if the submission was not followed by a redirect.

                                 #Example: After updating a homework's status, redirecting to the homework page ensures that if the user refreshes the page, the update won't be repeated.
                                

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')   #homework is url link



#-----------------------------------------------YouTube----------------------------------------------
from youtubesearchpython import VideosSearch

@login_required
def youtube(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']

        video=VideosSearch(text)
        result_list=[]

       # print(video.result())
        for i in video.result()['result']:
            result_dict={
                'input':text,                  #We did not use it in our template But we can use it to display the search query on the results page.
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],  #Bcoz it is list we can acces its elements using index only.
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }

            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)

            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    
    else:
          form=DashboardForm()
    context={'form':form}
    return render(request,"dashboard/youtube.html",context)



#--------------------------------------To-Do----------------------------------------

@login_required
def todo(request):
    if request.method=="POST":
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST["is_finished"]
                if finished == 'on':                 
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            
            todos=Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
            messages.success(request, f"Todo Added by {request.user.username}!!!")
    else:

         form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    all_completed = all(todo_item.is_finished for todo_item in todo)
    context={
        'form':form,
        'todos':todo,
        'todos_done':all_completed
        }
    return render(request,'dashboard/todo.html',context)


@login_required
def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False;
    else:
        todo.is_finished=True;
    todo.save()
    return redirect('todo')


@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')





#----------------------------BOOKS-----------------------------

import requests 

@login_required
def books(request):
     if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']

        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()

        # print(answer)
        result_list=[]


        for i in range(10):                                     #Iterates over the first 10 items
                    item = answer['items'][i]['volumeInfo']     #Retrieves the volumeInfo dictionary from each item in the items list.
                    result_dict = {
                        'title': item.get('title',''),          #The get method is used to safely access the value of the title key. If the key doesn’t exist, it prevents raising a KeyError and returns a default value instead.
                        'subtitle': item.get('subtitle',''),    #Similar to the title, this ensures that the code doesn’t fail if subtitle is missing and provides an empty string as a fallback.
                        'description': item.get('description',''),
                        'count': item.get('pageCount',''),
                        'categories': item.get('categories',[]),    #Since categories is a list, it’s important to use an empty list as the default to avoid errors when iterating over it in the template.
                        'rating': item.get('averageRating',''),
                        'thumbnail': item.get('imageLinks', {}).get('thumbnail',''),  #The get method is used twice here. First, it checks if imageLinks exists in item, and if it does, it tries to get thumbnail. This handles cases where imageLinks or thumbnail might be missing without raising errors.
                        'preview': item.get('previewLink',''),
                        'authors': item.get('authors', []),
                        'publisher': item.get('publisher', ''),
                        'publishedDate': item.get('publishedDate', '')
                    }
                    result_list.append(result_dict)
                    context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)
    
     else:
         form=DashboardForm()
     context={'form':form}
     return render(request,'dashboard/books.html',context)



#----------------------------------------Dictionary-------------------------------------
@login_required
def dictionary(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
        
        url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text   #Free API-Not Efficient
        r=requests.get(url)
        answer=r.json()
        
      
        if 'title' in answer and 'message' in answer:
                # API returned an error message
                context = {
                    'form': form,
                    'input': text,
                    'error': f"{answer['title']}: {answer['message']}"
                }
        else:
                phonetics=answer[0]['phonetics'][0].get('text','')
                audio=answer[0]['phonetics'][0].get('audio','')
                definition=answer[0]['meanings'][0]['definitions'][2].get('definition','')   #we want first definition from definitions
                example=answer[0]['meanings'][0]['definitions'][2].get('example','')
        
                
                context={
                'form':form,
                'input':text,
                'phonetics':phonetics,         #We are passing everything individually here because there is no multiple data.Every Dictionary Search Result is 1.
                'audio':audio,                 #So we do not used for loop and do not store data inside a list.
                'definition':definition,
                'example':example,
                 }
        return render(request,"dashboard/dictionary.html",context)
    else:    
        form=DashboardForm()
    context={'form':form}
    return render(request,"dashboard/dictionary.html",context)





#----------------------------------WIKIPEDIA-------------------------------

def filter_relevant_image(images, query):
    query = query.lower()
    relevant_images = []
    
    for image in images:
        if query in image.lower():
            relevant_images.append(image)
    
    return relevant_images


import wikipedia as wiki
import aiohttp
import asyncio
async def fetch_wikipedia_page(text):
    async with aiohttp.ClientSession() as session:
        try:
            search = wiki.page(text)
            return search
        except Exception as e:
            raise Exception("Error fetching the Wikipedia page")
        
@login_required
def wikipedia(request):
    if request.method=="POST":
        text = request.POST.get('text', '').strip()  # Strip any leading/trailing whitespace
        from_option = request.POST.get('from_option', 'no') == 'yes'  # Check if the input is from an option

        form=DashboardForm()
        
        if ' ' in text and not from_option:
            error_message = 'Please enter the search query without spaces.'
            context = {
                'form': form,
                'wrong': error_message,
            }
            return render(request, "dashboard/wiki.html", context)
        try:
           search = asyncio.run(fetch_wikipedia_page(text))
           images = search.images
           filtered_images = filter_relevant_image(images, text)
           # Getting the first filtered image URL if available
          
           image_url = images[0] if images else None
           context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary,
            'image_url':image_url,
            }
        except wiki.DisambiguationError as e:
            options = e.options
            context = {
                'form': form,
                'options': options,
            }
        except wiki.PageError:
            context = {
                'form': form,
                'error': 'The page does not exist. Please try another search term.',
            }
        except requests.exceptions.Timeout:
            context = {
                'form': form,
                'error': 'The request timed out. Please try again later.',
            }
        except Exception as e:
            context = {
                'form': form,
                'error': 'An error occurred. Please try again.',
            }
        return render(request,'dashboard/wiki.html',context)
    else:
        form=DashboardForm()
        context={
            'form':form
        }
    return render(request, "dashboard/wiki.html",context)



#----------------------------------Conversions-------------------------------
@login_required
def conversion(request):
    
    form = ConversionForm()  # Initialize the base form
    
    if request.method=="POST":
        form=ConversionForm(request.POST)
        measurement = request.POST.get('measurement')
        context = {'form':form, 'input':True}
       
        
        if measurement=='length':
            measurement_form = ConversionLengthForm(request.POST)
            context={'m_form':measurement_form}
            
        
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if first and second and input:
                        try:
                            input_value= float(input) 
                            # Conversion factors
                            conversion_factors = {
                                'yard': {'foot': 3, 'kilometre': 0.0009144, 'metre': 0.9144, 'centimetre': 91.44, 'millimetre': 914.4, 'micrometre': 914400, 'nanometre': 9.144e8, 'mile': 0.000568182, 'inch': 36},
                                'foot': {'yard': 1/3, 'kilometre': 0.0003048, 'metre': 0.3048, 'centimetre': 30.48, 'millimetre': 304.8, 'micrometre': 304800, 'nanometre': 3.048e8, 'mile': 0.000189394, 'inch': 12},
                                'kilometre': {'yard': 1094, 'foot': 3280.84, 'metre': 1000, 'centimetre': 100000, 'millimetre': 1000000, 'micrometre': 1e9, 'nanometre': 1e12, 'mile': 0.621371, 'inch': 39370.1},
                                'metre': {'yard': 1.09361, 'foot': 3.28084, 'kilometre': 0.001, 'centimetre': 100, 'millimetre': 1000, 'micrometre': 1e6, 'nanometre': 1e9, 'mile': 0.000621371, 'inch': 39.3701},
                                'centimetre': {'yard': 0.0109361, 'foot': 0.0328084, 'kilometre': 1e-5, 'metre': 0.01, 'millimetre': 10, 'micrometre': 10000, 'nanometre': 1e7, 'mile': 6.2137e-6, 'inch': 0.393701},
                                'millimetre': {'yard': 0.00109361, 'foot': 0.00328084, 'kilometre': 1e-6, 'metre': 0.001, 'centimetre': 0.1, 'micrometre': 1000, 'nanometre': 1e6, 'mile': 6.2137e-7, 'inch': 0.0393701},
                                'micrometre': {'yard': 1.0936e-6, 'foot': 3.2808e-6, 'kilometre': 1e-9, 'metre': 1e-6, 'centimetre': 1e-4, 'millimetre': 1e-3, 'nanometre': 1000, 'mile': 6.2137e-10, 'inch': 3.937e-5},
                                'nanometre': {'yard': 1.0936e-9, 'foot': 3.2808e-9, 'kilometre': 1e-12, 'metre': 1e-9, 'centimetre': 1e-7, 'millimetre': 1e-6, 'micrometre': 1e-3, 'mile': 6.2137e-13, 'inch': 3.937e-8},
                                'mile': {'yard': 1760, 'foot': 5280, 'kilometre': 1.60934, 'metre': 1609.34, 'centimetre': 160934, 'millimetre': 1609340, 'micrometre': 1.60934e9, 'nanometre': 1.60934e12, 'inch': 63360},
                                'inch': {'yard': 1/36, 'foot': 1/12, 'kilometre': 0.0000254, 'metre': 0.0254, 'centimetre': 2.54, 'millimetre': 25.4, 'micrometre': 25400, 'nanometre': 2.54e7, 'mile': 1.5783e-5}
                            }
                           

                            if first in conversion_factors and second in conversion_factors[first]:
                                conversion_factor = conversion_factors[first][second]
                                converted_value = input_value * conversion_factor

                                if converted_value.is_integer():
                                  converted_value = int(converted_value)
                                else:
                                   converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')
                                answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'

                        except ValueError:
                           answer = 'Invalid input value'

            context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        
        

        elif measurement=='mass':
            measurement_form = ConversionMassForm(request.POST)
            context['m_form'] = measurement_form
             
            
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if input:
                try:
                    input_value = float(input)

                    # Conversion factors
                    conversion_factors = {
                        'pound': {'kilogram': 0.453592, 'gram': 453.592, 'tonne': 0.000453592, 'milligram': 453592, 'microgram': 453592000, 'us_ton': 0.000446428, 'stone': 0.0714286, 'ounce': 16},
                        'kilogram': {'pound': 2.20462, 'gram': 1000, 'tonne': 0.001, 'milligram': 1000000, 'microgram': 1e6, 'us_ton': 0.000984207, 'stone': 0.157473, 'ounce': 35.274},
                        'gram': {'pound': 0.00220462, 'kilogram': 0.001, 'tonne': 1e-6, 'milligram': 1000, 'microgram': 1e6, 'us_ton': 2.20462e-7, 'stone': 0.000157473, 'ounce': 0.035274},
                        'tonne': {'pound': 2204.62, 'kilogram': 1000, 'gram': 1e6, 'milligram': 1e9, 'microgram': 1e12, 'us_ton': 1.10231, 'stone': 157.473, 'ounce': 35274},
                        'milligram': {'pound': 0.00000220462, 'kilogram': 0.000001, 'gram': 0.001, 'tonne': 1e-9, 'microgram': 1000, 'us_ton': 2.20462e-10, 'stone': 1.57473e-7, 'ounce': 3.5274e-5},
                        'microgram': {'pound': 2.20462e-9, 'kilogram': 1e-9, 'gram': 1e-6, 'tonne': 1e-12, 'milligram': 1e-3, 'us_ton': 2.20462e-13, 'stone': 1.57473e-10, 'ounce': 3.5274e-8},
                        'us_ton': {'pound': 2000, 'kilogram': 907.185, 'gram': 907185, 'tonne': 0.907185, 'milligram': 9.07185e5, 'microgram': 9.07185e8, 'stone': 142.857, 'ounce': 32000},
                        'stone': {'pound': 14, 'kilogram': 6.35029, 'gram': 6350.29, 'tonne': 0.00635029, 'milligram': 6350290, 'microgram': 6.35029e6, 'us_ton': 0.00446429, 'ounce': 224},
                        'ounce': {'pound': 0.0625, 'kilogram': 0.0283495, 'gram': 28.3495, 'tonne': 0.0000283495, 'milligram': 28349.5, 'microgram': 2.83495e7, 'us_ton': 0.00003125, 'stone': 0.00446429}
                    }

                    if first in conversion_factors and second in conversion_factors[first]:
                        conversion_factor = conversion_factors[first][second]
                        converted_value = input_value * conversion_factor
                        # Check if the converted value should be formatted as an integer
                        if converted_value.is_integer():
                            converted_value = int(converted_value)
                        else:
                            converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')
                        input_value_formatted = int(input_value) if input_value.is_integer() else input_value
                        answer = f'{input_value_formatted} {first} = {converted_value} {second}'
                        
                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }





        elif measurement=='time':
            measurement_form = ConversionTimeForm(request.POST)
            context['m_form'] = measurement_form
             
           
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if input:
                try:
                    input_value = float(input)

                    # Conversion factors
                    conversion_factors = {
                        'second': {'nanosecond': 1e9, 'microsecond': 1e6, 'millisecond': 1e3, 'minute': 1/60, 'hour': 1/3600, 'day': 1/86400, 'week': 1/604800, 'month': 1/2629746, 'calendar_year': 1/31557600, 'decade': 1/315576000, 'century': 1/3155760000},
                        'nanosecond': {'second': 1e-9, 'microsecond': 1e-6, 'millisecond': 1e-3, 'minute': 1.6667e-11, 'hour': 2.7778e-13, 'day': 1.1574e-14, 'week': 1.6534e-15, 'month': 3.8052e-16, 'calendar_year': 3.1688e-17, 'decade': 3.1688e-18, 'century': 3.1688e-19},
                        'microsecond': {'second': 1e-6, 'nanosecond': 1e3, 'millisecond': 1e-3, 'minute': 1.6667e-8, 'hour': 2.7778e-10, 'day': 1.1574e-11, 'week': 1.6534e-12, 'month': 3.8052e-13, 'calendar_year': 3.1688e-14, 'decade': 3.1688e-15, 'century': 3.1688e-16},
                        'millisecond': {'second': 1e-3, 'nanosecond': 1e6, 'microsecond': 1e3, 'minute': 1.6667e-5, 'hour': 2.7778e-7, 'day': 1.1574e-8, 'week': 1.6534e-9, 'month': 3.8052e-10, 'calendar_year': 3.1688e-11, 'decade': 3.1688e-12, 'century': 3.1688e-13},
                        'minute': {'second': 60, 'nanosecond': 6e10, 'microsecond': 6e7, 'millisecond': 6e4, 'hour': 1/60, 'day': 1/1440, 'week': 1/10080, 'month': 1/43800, 'calendar_year': 1/525600, 'decade': 1/5256000, 'century': 1/52560000},
                        'hour': {'second': 3600, 'nanosecond': 3.6e12, 'microsecond': 3.6e9, 'millisecond': 3.6e6, 'minute': 60, 'day': 1/24, 'week': 1/168, 'month': 1/730, 'calendar_year': 1/8760, 'decade': 1/87600, 'century': 1/876000},
                        'day': {'second': 86400, 'nanosecond': 8.64e13, 'microsecond': 8.64e10, 'millisecond': 8.64e7, 'minute': 1440, 'hour': 24, 'week': 1/7, 'month': 1/30, 'calendar_year': 1/365, 'decade': 1/3650, 'century': 1/36500},
                        'week': {'second': 604800, 'nanosecond': 6.048e14, 'microsecond': 6.048e11, 'millisecond': 6.048e8, 'minute': 10080, 'hour': 168, 'day': 7, 'month': 1/4.345, 'calendar_year': 1/52.1429, 'decade': 1/521.429, 'century': 1/5214.29},
                        'month': {'second': 2629746, 'nanosecond': 2.629746e15, 'microsecond': 2.629746e12, 'millisecond': 2.629746e9, 'minute': 43800, 'hour': 730, 'day': 30, 'week': 4.345, 'calendar_year': 1/12, 'decade': 1/120, 'century': 1/1200},
                        'calendar_year': {'second': 31557600, 'nanosecond': 3.15576e16, 'microsecond': 3.15576e13, 'millisecond': 3.15576e10, 'minute': 525600, 'hour': 8760, 'day': 365, 'week': 52.1429, 'month': 12, 'decade': 1/10, 'century': 1/100},
                        'decade': {'second': 315576000, 'nanosecond': 3.15576e17, 'microsecond': 3.15576e14, 'millisecond': 3.15576e11, 'minute': 5256000, 'hour': 87600, 'day': 3650, 'week': 521.429, 'month': 120, 'calendar_year': 10, 'century': 1/10},
                        'century': {'second': 3155760000, 'nanosecond': 3.15576e18, 'microsecond': 3.15576e15, 'millisecond': 3.15576e12, 'minute': 52560000, 'hour': 876000, 'day': 36500, 'week': 5214.29, 'month': 1200, 'calendar_year': 100, 'decade': 10}
                    }

                    if first in conversion_factors and second in conversion_factors[first]:
                        conversion_factor = conversion_factors[first][second]
                        converted_value = input_value * conversion_factor
                        # Check if the converted value should be formatted as an integer
                        if converted_value.is_integer():
                            converted_value = int(converted_value)
                        else:
                              converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')
                        answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'
                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }





        elif measurement=='volume':
            measurement_form = ConversionVolumeForm(request.POST)
            context['m_form'] = measurement_form
             
            
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if input:
                try:
                    input_value = float(input)

                    # Conversion factors
                    conversion_factors = {
                        'litre': {'millilitre': 1000, 'cubic_metre': 0.001, 'cubic_foot': 0.0353147, 'cubic_inch': 61.0237},
                        'millilitre': {'litre': 0.001, 'cubic_metre': 1e-6, 'cubic_foot': 3.53147e-5, 'cubic_inch': 0.0610237},
                        'cubic_metre': {'litre': 1000, 'millilitre': 1e6, 'cubic_foot': 35.3147, 'cubic_inch': 61023.7},
                        'cubic_foot': {'litre': 28.3168, 'millilitre': 28316.8, 'cubic_metre': 0.0283168, 'cubic_inch': 1728},
                        'cubic_inch': {'litre': 0.0163871, 'millilitre': 16.3871, 'cubic_metre': 1.63871e-5, 'cubic_foot': 0.000578704}
                    }

                    if first in conversion_factors and second in conversion_factors[first]:
                        conversion_factor = conversion_factors[first][second]
                        converted_value = input_value * conversion_factor

                        # Check if the converted value should be formatted as an integer
                        if converted_value.is_integer():
                            converted_value = int(converted_value)
                        else:
                             converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')
                        answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'
                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }



        elif measurement=='area':
            measurement_form = ConversionAreaForm(request.POST)
            context['m_form'] = measurement_form
             
            
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if input:
                try:
                    input_value = float(input)

                    # Conversion factors
                    conversion_factors = {
                            'square_metre': {'square_kilometre': 1e-6, 'square_mile': 3.861e-7, 'square_yard': 1.19599, 'square_foot': 10.7639, 'square_inch': 1550.0031, 'hectare': 1e-4, 'acre': 2.47105},
                            'square_kilometre': {'square_metre': 1e6, 'square_mile': 0.386102, 'square_yard': 1.19599e6, 'square_foot': 1.07639e7, 'square_inch': 1.5500031e9, 'hectare': 100, 'acre': 247.105},
                            'square_mile': {'square_metre': 2.58999e6, 'square_kilometre': 2.58999, 'square_yard': 2.785e6, 'square_foot': 2.788e7, 'square_inch': 4.014e9, 'hectare': 258.999, 'acre': 640},
                            'square_yard': {'square_metre': 0.836127, 'square_kilometre': 8.36127e-7, 'square_mile': 3.2283e-7, 'square_foot': 9, 'square_inch': 1296, 'hectare': 8.36127e-5, 'acre': 2.2957e-4},
                            'square_foot': {'square_metre': 0.092903, 'square_kilometre': 9.2903e-8, 'square_mile': 3.587e-8, 'square_yard': 0.111111, 'square_inch': 144, 'hectare': 9.2903e-6, 'acre': 2.2957e-5},
                            'square_inch': {'square_metre': 0.00064516, 'square_kilometre': 6.4516e-10, 'square_mile': 2.491e-10, 'square_yard': 0.000771605, 'square_foot': 0.00694444, 'hectare': 6.4516e-8, 'acre': 1.5942e-7},
                            'hectare': {'square_metre': 1e4, 'square_kilometre': 0.01, 'square_mile': 0.00386102, 'square_yard': 11959.9, 'square_foot': 107639.1, 'square_inch': 15500031, 'acre': 2.47105},
                            'acre': {'square_metre': 4046.86, 'square_kilometre': 0.00404686, 'square_mile': 0.0015625, 'square_yard': 4840, 'square_foot': 43560, 'square_inch': 6272640, 'hectare': 0.404686}
                    }

                    if first in conversion_factors and second in conversion_factors[first]:
                        conversion_factor = conversion_factors[first][second]
                        converted_value = input_value * conversion_factor

                        # Check if the converted value should be formatted as an integer
                        if converted_value.is_integer():
                            converted_value = int(converted_value)
                        else:
                                converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')

                        answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'
                        
                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }





        elif measurement=='temperature':
            measurement_form = ConversionTemperatureForm(request.POST)
            context['m_form'] = measurement_form
              
            
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if input:
                try:
                    input_value = float(input)
                    converted_value=None

                    if first == 'celsius':
                        if second == 'kelvin':
                            converted_value = input_value + 273.15
                        elif second == 'fahrenheit':
                            converted_value = (input_value * 9/5) + 32
                        else:
                            converted_value = input_value

                    elif first == 'kelvin':
                         if second == 'celsius':
                            converted_value = input_value - 273.15
                         elif second == 'fahrenheit':
                            converted_value = ((input_value - 273.15) * 9/5) + 32
                         else:
                            converted_value = input_value

                    elif first == 'fahrenheit':
                        if second == 'celsius':
                            converted_value = (input_value - 32) * 5/9
                        elif second == 'kelvin':
                            converted_value = ((input_value - 32) * 5/9) + 273.15
                        else:
                            converted_value = input_value
                    if converted_value is not None:
                      if converted_value.is_integer():
                         converted_value = int(converted_value)
                      else:
                        converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')
                      answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'
                    

                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }


        elif measurement=='digital storage':
            measurement_form = ConversionDigitalStorageForm(request.POST)
            context['m_form'] = measurement_form
              
           
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if input:
                try:
                    input_value = float(input)

                    # Conversion factors
                    conversion_factors = {
                        'byte': {'kilobyte': 1e-3, 'megabyte': 1e-6, 'gigabyte': 1e-9, 'terabyte': 1e-12, 'petabyte': 1e-15, 'bit': 8, 'kilobit': 8e-3, 'megabit': 8e-6, 'gigabit': 8e-9, 'terabit': 8e-12, 'petabit': 8e-15},
                            'kilobyte': {'byte': 1000, 'megabyte': 1e-3, 'gigabyte': 1e-6, 'terabyte': 1e-9, 'petabyte': 1e-12, 'bit': 8000, 'kilobit': 8, 'megabit': 0.008, 'gigabit': 8e-6, 'terabit': 8e-9, 'petabit': 8e-12},
                            'megabyte': {'byte': 1e6, 'kilobyte': 1000, 'gigabyte': 1e-3, 'terabyte': 1e-6, 'petabyte': 1e-9, 'bit': 8e6, 'kilobit': 8000, 'megabit': 8, 'gigabit': 0.008, 'terabit': 8e-11, 'petabit': 8e-14},
                            'gigabyte': {'byte': 1e9, 'kilobyte': 1e6, 'megabyte': 1000, 'terabyte': 1e-3, 'petabyte': 1e-6, 'bit': 8e9, 'kilobit': 8e6, 'megabit': 8000, 'gigabit': 8, 'terabit': 0.008, 'petabit': 8e-11},
                            'terabyte': {'byte': 1e12, 'kilobyte': 1e9, 'megabyte': 1e6, 'gigabyte': 1000, 'petabyte': 1e-3, 'bit': 8e12, 'kilobit': 8e9, 'megabit': 8e6, 'gigabit': 8000, 'terabit': 8, 'petabit': 8e-9},
                            'petabyte': {'byte': 1e15, 'kilobyte': 1e12, 'megabyte': 1e9, 'gigabyte': 1e6, 'terabyte': 1000, 'bit': 8e15, 'kilobit': 8e12, 'megabit': 8e9, 'gigabit': 8e6, 'terabit': 8000, 'petabit': 8},
                            'bit': {'byte': 1/8, 'kilobyte': 1e-3/8, 'megabyte': 1e-6/8, 'gigabyte': 1e-9/8, 'terabyte': 1e-12/8, 'petabyte': 1e-15/8, 'kilobit': 1e-3, 'megabit': 1e-6, 'gigabit': 1e-9, 'terabit': 1e-12, 'petabit': 1e-15},
                            'kilobit': {'byte': 1/8e-3, 'kilobyte': 1e-3, 'megabyte': 1e-6, 'gigabyte': 1e-9, 'terabyte': 1e-12, 'petabyte': 1e-15, 'bit': 1000, 'megabit': 1e-3, 'gigabit': 1e-6, 'terabit': 1e-9, 'petabit': 1e-12},
                            'megabit': {'byte': 1/8e-6, 'kilobyte': 1e-3/8, 'megabyte': 1e-6, 'gigabyte': 1e-9, 'terabyte': 1e-12, 'petabyte': 1e-15, 'bit': 1e6, 'kilobit': 1000, 'gigabit': 1e-3, 'terabit': 1e-6, 'petabit': 1e-9},
                            'gigabit': {'byte': 1/8e-9, 'kilobyte': 1e-3/8e6, 'megabyte': 1e-6/8, 'gigabyte': 1e-9, 'terabyte': 1e-12, 'petabyte': 1e-15, 'bit': 1e9, 'kilobit': 1e6, 'megabit': 1000, 'terabit': 1e-3, 'petabit': 1e-6},
                            'terabit': {'byte': 1/8e-12, 'kilobyte': 1e-3/8e9, 'megabyte': 1e-6/8e6, 'gigabyte': 1e-9/8, 'terabyte': 1e-12, 'petabyte': 1e-15, 'bit': 1e12, 'kilobit': 1e9, 'megabit': 1e6, 'gigabit': 1000, 'petabit': 1e-3},
                            'petabit': {'byte': 1/8e-15, 'kilobyte': 1e-3/8e12, 'megabyte': 1e-6/8e9, 'gigabyte': 1e-9/8e6, 'terabyte': 1e-12/8e3, 'petabyte': 1e-15, 'bit': 1e15, 'kilobit': 1e12, 'megabit': 1e9, 'gigabit': 1e6, 'terabit': 1000}
                    }

                    if first in conversion_factors and second in conversion_factors[first]:
                        conversion_factor = conversion_factors[first][second]
                        converted_value = input_value * conversion_factor

                        # Check if the converted value should be formatted as an integer
                        if converted_value.is_integer():
                            converted_value = int(converted_value)
                        else:
                            converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')

                        answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'
                        
                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }


        elif measurement=='energy':
            measurement_form = ConversionEnergyForm(request.POST)
            context['m_form'] = measurement_form
            
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if input:
                try:
                    input_value = float(input)

                    # Conversion factors
                    conversion_factors = {
                        'joule': {'kilojoule': 1e-3, 'calorie': 0.239006, 'kilocalorie': 0.000239006, 'watt_hour': 2.77778e-4, 'kilowatt_hour': 2.77778e-7, 'electronvolt': 6.242e+18, 'foot_pound': 0.737562},
                            'kilojoule': {'joule': 1000, 'calorie': 239.006, 'kilocalorie': 0.239006, 'watt_hour': 0.277778, 'kilowatt_hour': 0.000277778, 'electronvolt': 6.242e+21, 'foot_pound': 737.562},
                            'calorie': {'joule': 4.184, 'kilojoule': 0.004184, 'kilocalorie': 0.001, 'watt_hour': 0.001163, 'kilowatt_hour': 1.163e-6, 'electronvolt': 2.611e+19, 'foot_pound': 0.003086},
                            'kilocalorie': {'joule': 4184, 'kilojoule': 4.184, 'calorie': 1000, 'watt_hour': 1.163, 'kilowatt_hour': 0.001163, 'electronvolt': 2.611e+22, 'foot_pound': 3.086},
                            'watt_hour': {'joule': 3600, 'kilojoule': 3.6, 'calorie': 859.845, 'kilocalorie': 0.859845, 'kilowatt_hour': 0.001, 'electronvolt': 2.25e+22, 'foot_pound': 2655.23},
                            'kilowatt_hour': {'joule': 3.6e6, 'kilojoule': 3600, 'calorie': 3.6e6, 'kilocalorie': 3600, 'watt_hour': 1000, 'electronvolt': 2.25e+25, 'foot_pound': 2.655e6},
                            'electronvolt': {'joule': 1.602e-19, 'kilojoule': 1.602e-16, 'calorie': 3.821e-18, 'kilocalorie': 3.821e-21, 'watt_hour': 4.450e-22, 'kilowatt_hour': 4.450e-25, 'foot_pound': 1.188e-19},
                            'foot_pound': {'joule': 1.35582, 'kilojoule': 0.00135582, 'calorie': 0.322081, 'kilocalorie': 0.000322081, 'watt_hour': 0.000377, 'kilowatt_hour': 3.77e-7, 'electronvolt': 2.170e+16},
                    }

                    if first in conversion_factors and second in conversion_factors[first]:
                        conversion_factor = conversion_factors[first][second]
                        converted_value = input_value * conversion_factor

                        # Check if the converted value should be formatted as an integer
                        if converted_value.is_integer():
                            converted_value = int(converted_value)
                        else:
                            converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')

                        answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'
                        
                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }


        elif measurement=='speed':
            measurement_form = ConversionSpeedForm(request.POST)
            context['m_form'] = measurement_form
              
           
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if input:
                try:
                    input_value = float(input)

                    # Conversion factors
                    conversion_factors = {
                        'metre_per_second': {'mile_per_hour': 2.23694, 'foot_per_second': 3.28084, 'kilometre_per_hour': 3.6, 'knot': 1.94384},
                            'mile_per_hour': {'metre_per_second': 0.44704, 'foot_per_second': 1.46667, 'kilometre_per_hour': 1.60934, 'knot': 0.868976},
                            'foot_per_second': {'metre_per_second': 0.3048, 'mile_per_hour': 0.681818, 'kilometre_per_hour': 1.09728, 'knot': 0.592484},
                            'kilometre_per_hour': {'metre_per_second': 0.277778, 'mile_per_hour': 0.621371, 'foot_per_second': 0.911344, 'knot': 0.539957},
                            'knot': {'metre_per_second': 0.514444, 'mile_per_hour': 1.15078, 'foot_per_second': 1.68781, 'kilometre_per_hour': 1.852},
                            
                    }

                    if first in conversion_factors and second in conversion_factors[first]:
                        conversion_factor = conversion_factors[first][second]
                        converted_value = input_value * conversion_factor

                        # Check if the converted value should be formatted as an integer
                        if converted_value.is_integer():
                            converted_value = int(converted_value)
                        else:
                            converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')

                        answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'
                        
                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }


        elif measurement=='pressure':
            measurement_form = ConversionPressureForm(request.POST)
            context['m_form'] = measurement_form
              
            
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
                
            if input:
                try:
                    input_value = float(input)

                    # Conversion factors
                    conversion_factors = {
                            'bar': {'pascal': 100000, 'torr': 750.062, 'standard_atmosphere': 0.986923, 'psi': 14.5038},
                            'pascal': {'bar': 1e-5, 'torr': 0.00750062, 'standard_atmosphere': 9.8692e-6, 'psi': 0.000145038},
                            'torr': {'bar': 0.00133322, 'pascal': 133.322, 'standard_atmosphere': 0.00131579, 'psi': 0.0193368},
                            'standard_atmosphere': {'bar': 1.01325, 'pascal': 101325, 'torr': 760, 'psi': 14.696},
                            'psi': {'bar': 0.0689476, 'pascal': 6894.76, 'torr': 51.7149, 'standard_atmosphere': 0.068046},
                    }

                    if first in conversion_factors and second in conversion_factors[first]:
                        conversion_factor = conversion_factors[first][second]
                        converted_value = input_value * conversion_factor

                        # Check if the converted value should be formatted as an integer
                        if converted_value.is_integer():
                            converted_value = int(converted_value)
                        else:
                            converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')

                        answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'
                        
                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }



        elif measurement=='frequency':
            measurement_form = ConversionFrequencyForm(request.POST)
            context['m_form'] = measurement_form
            
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if input:
                try:
                    input_value = float(input)

                    # Conversion factors
                    conversion_factors = {
                            'hertz': {'kilohertz': 1e-3, 'megahertz': 1e-6, 'gigahertz': 1e-9},
                            'kilohertz': {'hertz': 1e3, 'megahertz': 1e-3, 'gigahertz': 1e-6},
                            'megahertz': {'hertz': 1e6, 'kilohertz': 1e3, 'gigahertz': 1e-3},
                            'gigahertz': {'hertz': 1e9, 'kilohertz': 1e6, 'megahertz': 1e3},
                    }

                    if first in conversion_factors and second in conversion_factors[first]:
                        conversion_factor = conversion_factors[first][second]
                        converted_value = input_value * conversion_factor

                        # Check if the converted value should be formatted as an integer
                        if converted_value.is_integer():
                            converted_value = int(converted_value)
                        else:
                            converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')

                        answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'
                        
                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }


        elif measurement=='plane angle':
            measurement_form = ConversionPlaneAngleForm(request.POST)
            context['m_form'] = measurement_form
            
            
            first=request.POST.get('measure1')
            second=request.POST.get('measure2')
            input=request.POST.get('input')
            answer=''
            if input:
                try:
                    input_value = float(input)

                    # Conversion factors
                    conversion_factors = {
                        'degree': {'gradian': 1.11111, 'radian': 0.0174533, 'milliradian': 17.4533, 'minute_of_arc': 60},
                            'gradian': {'degree': 0.9, 'radian': 0.0157079, 'milliradian': 15.7079, 'minute_of_arc': 54},
                            'radian': {'degree': 57.2958, 'gradian': 63.661977, 'milliradian': 1000, 'minute_of_arc': 3437.75},
                            'milliradian': {'degree': 0.0572958, 'gradian': 0.063661977, 'radian': 0.001, 'minute_of_arc': 3.43775},
                            'minute_of_arc': {'degree': 0.0166667, 'gradian': 0.0185185, 'radian': 0.000290888, 'milliradian': 0.290888}
                    }

                    if first in conversion_factors and second in conversion_factors[first]:
                        conversion_factor = conversion_factors[first][second]
                        converted_value = input_value * conversion_factor

                        # Check if the converted value should be formatted as an integer
                        if converted_value.is_integer():
                            converted_value = int(converted_value)
                        else:
                            converted_value = "{:.10f}".format(converted_value).rstrip('0').rstrip('.')

                        answer = f'{int(input_value) if input_value.is_integer() else input_value} {first} = {converted_value} {second}'
                        
                except ValueError:
                    answer = 'Invalid input value'
                
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
           
    else:
        form=ConversionForm()
        context={
        'form':form,
        'input':False    #optional
         }
    return render(request,"dashboard/conversion.html",context)





#-----------------------------------Registration------------------------------------
def register(request):

    if request.method == "POST":
        form=UserRegistrationForm(request.POST)  #When the form is submitted (via a POST request), UserRegistrationForm(request.POST) creates an instance of the form with the submitted data.
        if form.is_valid():
            form.save()                          #creates a new user in the database using the provided username and password.
            username=form.cleaned_data.get('username')
            messages.success(request, f"Account Created Successfully for {username} !!")
            return redirect('login')
            


    else:
         form=UserRegistrationForm()
    context={
        'form':form
    }
    return render(request,'dashboard/register.html',context)

@login_required
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False, user=request.user)
    todos=Todo.objects.filter(is_finished=False,user=request.user)

    all_completed_homework = all(hw_item.is_finished for hw_item in homeworks)  # Check if all homework items are completed
    all_completed_todo = all(todo_item.is_finished for todo_item in todos)

    context={'homework':homeworks, 
             'homeworks_done':all_completed_homework,
             'todo':todos,
             'todos_done':all_completed_todo
             }
    return render(request, 'dashboard/profile.html',context)





