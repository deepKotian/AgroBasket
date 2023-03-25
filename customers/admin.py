from django.contrib import admin
from customers.models import CompleteProfile, Products,Cart,Cartitems,OrderItem
# Register your models here.
admin.site.register(CompleteProfile)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(OrderItem)
