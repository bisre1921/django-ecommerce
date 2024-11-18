from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
    
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(default=0 , max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , default=1)
    description = models.TextField(default='' , blank=True , null=True)
    image = models.ImageField(upload_to='uploads/products/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0 , max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    address = models.CharField(max_length=100 , default='', blank=True)
    phone = models.CharField(max_length=20 , default='', blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for {self.customer.first_name} {self.customer.last_name}"
    