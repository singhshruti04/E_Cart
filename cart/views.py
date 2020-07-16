from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, ProductCart, OrderProduct, ListedProduct, Wishlist
from .forms import LoginForm, RegisterationForm
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login_view(request):
    next =request.GET.get('next')
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect('home')
        return redirect('home')
        

    context = {
        'form': form,
    }
    return render(request, "cart/login.html", context)

def register_view(request):
    next =request.GET.get('next')
    form = RegisterationForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save( )
        user = authenticate(email=email, password=password)      
        if next:
            return redirect('login')
        return redirect('login')

    context = {
        'form': form,
    }
    return render(request, "cart/register.html", context)

@login_required
def home_view(request):
    electronics_list = Product.objects.filter(category="Electronics")[:5]
    clothing_list = Product.objects.filter(category="Clothing")[:5]
    stationary_list = Product.objects.filter(category="Stationary")[:5]
    home_list = Product.objects.filter(category="Home_and_appliances")[:5]
    return render(request, 'cart/home.html', 
        {'users': User.objects.exclude(username=request.user.username), 
        'clothing_list': clothing_list,
        'electronics_list': electronics_list,
        'stationary_list': stationary_list,
        'home_list': home_list}) 

def cart_list_views(request):
    cart_qs = ProductCart.objects.filter(
        customer=request.user, 
        ordered=False)

    if cart_qs.exists():
        cart = cart_qs[0]

        print(cart)
        if cart.product.exists():
            order_product=OrderProduct.objects.filter(
                customer= request.user,
                ordered =False
                )
            print(order_product)
            return render(request, "cart/cart_list.html",{
                'product_list':order_product
                })
        else:
            return redirect('empty_cart')
    else:
        return redirect('empty_cart')

def wishlist_views(request):
    wishlist_qs = Wishlist.objects.filter(
        customer=request.user)

    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]

        if wishlist.product.exists():
            listed_product= ListedProduct.objects.filter(
                customer= request.user)
            print(listed_product)
            return render(request, "cart/wishlist.html",{
                'product_list':listed_product
                })
        else:
            return redirect('empty_wishlist')
    else:
        
        return redirect('empty_wishlist')




@login_required
def products_view(request):
    products_list = Product.objects.order_by('name')
    print(products_list)
    return render(request, 'cart/products.html', 
        {'users': User.objects.exclude(username=request.user.username), 
        'products_list': products_list})



@login_required
def products_category_view(request, slug):
    products_list = Product.objects.filter(category=slug)
    return render(request, 'cart/products.html', 
        {'users': User.objects.exclude(username=request.user.username), 
        'products_list': products_list})


@login_required
def detail_view(request, product_id):
    print(product_id)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    return render(request, 'cart/details.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        customer=request.user,
        ordered=False
        )
    cart_qs = ProductCart.objects.filter(customer=request.user, ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.product.filter(product_id=product.id).exists():
            order_product.quantity +=1
            order_product.save()
            messages.info(request, "This product quantity is updated in your cart.")
        else:
            messages.info(request, "This product is added to your cart.")
            cart.product.add(order_product)

    else:
        cart = ProductCart.objects.create(customer=request.user)
        cart.product.add(order_product)
        messages.info(request, "This product is added to your cart.")
    return redirect("cart_list_views")

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_qs = ProductCart.objects.filter(
        customer=request.user, 
        ordered=False)

    if cart_qs.exists():
        cart = cart_qs[0]

        print(cart)
        if cart.product.filter(product_id=product.id).exists():
            order_product= OrderProduct.objects.filter(
                product=product,
                customer= request.user,
                ordered =False
                )[0]
            if order_product.quantity>1:
                order_product.quantity-=1
                order_product.save()
            else:
                 order_product.delete()
            print(cart.product)
            messages.info(request, "This product is removed from your cart.")
        else:
            messages.info(request, "This product was not in your cart.")
            return redirect("cart_list_views")
    else:
        messages.info(request, "You do not have any product in your cart.")
        return redirect("cart_list_views")
    return redirect("cart_list_views")

@login_required
def empty_cart(request):
    return render(request, "cart/empty_cart.html", {})

@login_required
def empty_wishlist(request):
    return render(request, "cart/empty_wishlist.html", {})

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    listed_product, created = ListedProduct.objects.get_or_create(
        product=product,
        customer=request.user,
        )
    wishlist_qs = Wishlist.objects.filter(customer=request.user)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        if wishlist.product.filter(product_id=product.id).exists():
            messages.info(request, "This product is already exists in your Wishlist.")
        else:
            messages.info(request, "This product is added to your wishlist.")
            wishlist.product.add(listed_product)

    else:
        wishlist = Wishlist.objects.create(customer=request.user)
        wishlist.product.add(listed_product)
        messages.info(request, "This product is added to your Wishlist.")
    return redirect("products")

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_qs = Wishlist.objects.filter(
        customer=request.user)

    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]

        print(wishlist)
        if wishlist.product.filter(product_id=product.id).exists():
            listed_product= ListedProduct.objects.filter(
                product=product,
                customer= request.user,
                )[0]
            listed_product.delete()
            messages.info(request, "This product is removed from Wishlist.")
            return redirect("wishlist_views")
    else:
        return redirect("empty_wishlist")
    return redirect("wishlist_views")


