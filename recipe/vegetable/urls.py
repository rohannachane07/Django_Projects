from django.urls import path
from . import views


urlpatterns = [
    path('',views.recipes, name='view_recipe'),
    path('delete-recipe/<id>',views.delete_recipe, name='delete_recipe'),  #Dynamic URL
    path('update-recipe/<id>',views.update_recipe, name='update_recipe'),
    path('login/',views.login_page, name='login_page'),
    path('register/',views.register, name='reg_page'),
    path('logout/',views.logout_page, name='logout_page'),
]
