from django.contrib import admin
from customers.models import CompleteProfile, Products,Cart,Cartitems,OrderItem,Reviews,DeliveryProfile,Delivery
# Register your models here.
admin.site.register(CompleteProfile)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(OrderItem)
admin.site.register(Reviews)
admin.site.register(DeliveryProfile)
admin.site.register(Delivery)