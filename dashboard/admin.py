from django.contrib import admin
from . models import Homework, Notes, Todo
# Register your models here.
admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)