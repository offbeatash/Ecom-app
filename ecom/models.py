from django.db import models

# Create your models here.

class Student(models.Model):
    email = models.EmailField()
    name = models.CharField()


    def __str__(self):
        return self.email
    
    
class Img(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='test_imgs')
    

    def __str__(self):
        return self.name    
    
class Registration(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mob = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='cat_imgs')
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='prod_imgs')
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name