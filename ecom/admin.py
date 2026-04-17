from django.contrib import admin
from .models import *

# Register your models here.

class student_(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']

admin.site.register(Student, student_, )


class Img_(admin.ModelAdmin):
    list_display = ['id', 'name', 'image']

admin.site.register(Img, Img_, )

class reg_(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'mob','password']
admin.site.register(Registration, reg_, )

class cat_(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'description']
admin.site.register(Category, cat_, )

class prod_(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'price', 'stock', 'description', 'category']
admin.site.register(Product, prod_, )