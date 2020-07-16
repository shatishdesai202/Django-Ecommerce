from django.db import models
import datetime
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_all_category():
        return Category.objects.all()

    

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @staticmethod
    def get_all_product():
        return Product.objects.all()
    
    @staticmethod
    def get_product_filter(id):
        return Product.objects.filter(category=id)
    
    @staticmethod
    def get_product_detail(ids):
        return Product.objects.filter(id__in=ids)
    
    def __str__(self):
        return self.name
    

class Signup(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.first_name

    def is_exist(self):
        return Signup.objects.filter(email = self.email)
    
    @staticmethod
    def customer_check_by_email(email):
        try:
            return Signup.objects.get(email=email)
        except:
            return False
    @staticmethod
    def get_customer_detail(id):
        return Signup.objects.get(id=id)
            

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Signup, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.IntegerField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)
    

    @staticmethod
    def get_order_by_id(id):
        return Order.objects.filter(customer = id).order_by('-date')

    