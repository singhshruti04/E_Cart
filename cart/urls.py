from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [

  path('', views.login_view, name='login'),
  path('register', views.register_view, name='register'),
  path('home', views.home_view, name='home'),
  path('cart_list_views', views.cart_list_views, name='cart_list_views'),
  path('wishlist_views', views.wishlist_views, name='wishlist_views'),
  path('empty_cart', views.empty_cart, name='empty_cart'),
  path('empty_wishlist', views.empty_wishlist, name='empty_wishlist'),
  path('products', views.products_view, name='products'),
  path('<int:product_id>', views.detail_view, name='details'),
  path('checkout', views.checkout, name='checkout'),
  path('logout', LogoutView.as_view(next_page='login'), name='logout'),
  path('<slug:slug>', views.products_category_view, name='products_category'),
  path('add-to-cart/<int:product_id>', views.add_to_cart, name='add-to-cart'),
  path('remove-from-cart/<int:product_id>', views.remove_from_cart, name='remove-from-cart'),
  path('add-to-wishlist/<int:product_id>', views.add_to_wishlist, name='add-to-wishlist'),
  path('remove-from-wishlist/<int:product_id>', views.remove_from_wishlist, name='remove-from-wishlist'),


]

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 
