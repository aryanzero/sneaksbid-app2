from django.contrib import admin

from .models import Item, Bid, OrderItem, BillingAddress, Order, Payment2, Shoe , Profile, Brand

# Register your models here.
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(Order)
admin.site.register(Payment2)
admin.site.register(Shoe)
admin.site.register(Profile)
admin.site.register(Brand)