from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home,name='home'),       #name used for {% url 'home' %} in templates, for redirecting or linking to the home page
    path('add/',views.add_note,name='add_note'),
    path('edit/<int:note_id>/',views.edit_note,name='edit_note'),
    path('delete/<int:note_id>/',views.delete_note,name='delete_note'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
]



# LoginView.as_view(...)-Built-in Django class-based view that handles login form submission & validation.
# LogoutView.as_view(...)-Built-in view that handles logout (clears session/cookies).

# template_name and next_page are predefined (default) keyword arguments in Django’s class-based views like LoginView and LogoutView.

# template_name (used in LoginView)
# This tells Django:
# “Use this specific template file (like login.html) to render the login page.”
# 🧠 It’s used when Django needs to display a page (like a login form).

# next_page (used in LogoutView)
# This tells Django:
# “After this action (like logout), redirect the user to this page.”
# 🧠 It's used when Django needs to redirect the user, not show a page.