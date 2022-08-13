
from django.contrib import admin
from django.urls import path
# from views import *
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="home"),
    path('homework', homework,name="homework"),
    path('delete_homework/<int:pk>/<str:page>', delete_homework,name="delete_homework"),
    path('update_homework/<int:pk>', update_homework,name="update_homework"),
    path('notes', notes,name="notes"),
    path('delete_note/<int:pk>', delete_note,name="delete_note"),
    path('note_detail/<int:pk>', notedetail.as_view() ,name="note_detail"),
    path('youtube', youtube,name="youtube"),
    path('todo', todo,name="todo"),
    path('deletetodo/<int:pk>/<str:page>', deletetodo,name="deletetodo"),
    path('updatetodo/<int:pk>', updatetodo,name="updatetodo"),
    path('books', books,name="books"),
    path('dictionary', dictionary,name="dictionary"),
    path('wiki', wiki,name="wiki"),
    path('conversion', conversion,name="conversion"),
    path('profile', profile,name="profile"),

    

]
