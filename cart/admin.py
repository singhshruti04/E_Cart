from django.contrib import admin
from .models import Product, ProductCart, OrderProduct, ListedProduct, Wishlist

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductCart)
admin.site.register(OrderProduct)
admin.site.register(ListedProduct)
admin.site.register(Wishlist)


