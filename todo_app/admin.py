# Register your models here.
from django.contrib import admin
from .models import User,Todo

class Usercreate(admin.ModelAdmin):
    list_display = ['id','username','mobile','password']
    class Todoscreate(admin.ModelAdmin):
     list_display = ['id','owner','task','due_date','completed']
    admin.site.register(Todo,Todoscreate)
admin.site.register(User,Usercreate,)

