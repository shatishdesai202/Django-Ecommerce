from django.contrib import admin
from .models import Product, Category, Signup, Order
# Register your models here.


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'timestamp']


class AdminOrder(admin.ModelAdmin):
    list_display = ['product', 'customer', 'phone', 'date']


admin.site.register(Product, AdminProduct)
admin.site.register(Category)
admin.site.register(Signup)
admin.site.register(Order, AdminOrder)
