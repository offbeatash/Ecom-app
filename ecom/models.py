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

class Cart(models.Model):
    user = models.ForeignKey(Registration, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(Registration, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    
    total_amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=20) # cod or online
    payment_status = models.CharField(max_length=20, default='Pending') # Pending, Paid, Failed
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)