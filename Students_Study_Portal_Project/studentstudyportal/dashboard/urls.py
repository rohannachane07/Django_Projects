from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name='home'),

    #-------------------Notes----------------------
    path('notes',views.notes, name='notes'),
    path('delete_note/<int:pk>',views.delete_note, name='delete-note'),
    path('notes_detail/<int:pk>',views.notesDetailView.as_view(), name='notes-detail'),  # class-based view (CBV).

    #------------------HomeWork--------------------
    path('homework',views.homework,name='homework'),
    path('update_homework/<int:pk>',views.update_homework,name='update-homework'),
    path('delete_homework/<int:pk>',views.delete_homework,name='delete-homework'),



   #-----------------------Youtube-------------------
    path('youtube',views.youtube,name='youtube'),



    #-----------------------To-Do--------------------
    path('todo',views.todo,name='todo'),
    path('update_todo/<int:pk>',views.update_todo,name='update-todo'),
    path('delete_todo/<int:pk>',views.delete_todo,name='delete-todo'),



    
    #-----------------------Books--------------------
    path('books',views.books,name='books'),
    

    #-----------------------Dictionary---------------
    path('dictionary',views.dictionary,name='dictionary'),


     #-----------------------Wikipedia---------------
    path('wikipedia',views.wikipedia,name='wikipedia'),

    #-----------------------Conversion---------------
    path('conversion',views.conversion,name='conversion'),


  

   
]
