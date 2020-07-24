from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

class Product(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='images/')
	description = models.CharField(max_length=600)
	category = models.CharField(max_length=70)
	subcategory = models.CharField(max_length=70)
	gender = models.CharField(max_length=50)
	price = models.IntegerField()
	discount_price = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.name

	def get_add_to_cart_url(self):
		return reverse("add-to-cart",kwargs={
			'product_id':self.id
			})

	def get_remove_from_cart_url(self):
		return reverse("remove-from-cart",kwargs={
			'product_id':self.id
			})

	def get_add_to_wishlist_url(self):
		return reverse("add-to-wishlist",kwargs={
			'product_id':self.id
			})

	def get_remove_from_wishlist_url(self):
		return reverse("remove-from-wishlist",kwargs={
			'product_id':self.id
			})



class OrderProduct(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	ordered = models.BooleanField(default=False)


	def __str__(self):
		return f"{self.product.name}"

	def get_total_product_price(self):
		return self.quantity*self.product.price

	def get_total_product_discount_price(self):
		if self.product.discount_price > 0:
			return self.quantity*self.product.discount_price
		else:
			return self.quantity*self.product.price

class ProductCart(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ManyToManyField(OrderProduct)
	order_date = models.DateTimeField(auto_now_add=True)
	ordered = models.BooleanField(default=False)

	def __str__(self):
		return self.customer.username
		
	def get_total(self):
		total=0
		for cart_product in self.product.all():
			total += cart_product.get_total_product_price()
		return total

	def get_discount_total(self):
		total=0
		for cart_product in self.product.all():
			total += cart_product.get_total_product_discount_price()
		return total

	def get_saved(self):
		return self.get_discount_total() - self.get_total()

	def get_pay_total(self):
		return 300 + self.get_total()


	class Meta:
		ordering = ('order_date',)

class ListedProduct(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return f"{ self.product.name }"

class Wishlist(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ManyToManyField(ListedProduct)
	order_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.customer.username