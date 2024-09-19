from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.


def detail(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order ={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    context = {
        'products':products,
        'categories':categories,
        'active_category':active_category,
        'items': items, 
        'order': order, 
        'cartItems':cartItems,
        'user_not_login':user_not_login, 
        'user_login':user_login
    }
    return render(request, 'app/detail.html', context)


# def category(request):
#     categories = Category.objects.filter(is_sub=False)
#     active_category = request.GET.get('category','')
#     if active_category:
#         products = Product.objects.filter(category__slug = active_category)
#     context = {'categories':categories, 'products':products, 'active_category':active_category}
#     return render(request,'app/category.html', context)

def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    else:
        products = Product.objects.all()

    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category,
        'user_not_login': user_not_login,
        'user_login': user_login,
    }
    return render(request, 'app/category.html', context)


def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains =  searched)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order ={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"

    products = Product.objects.all()
    categories = Category.objects.filter(is_sub=False)
    return render(request,'app/search.html', {
        "searched":searched, 
        "keys":keys, 
        "products":products, 
        "cartItems":cartItems, 
        'user_not_login':user_not_login, 
        'user_login':user_login,
        'categories':categories
    })

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
        
    categories = Category.objects.filter(is_sub=False)
    context = {'form': form, 'user_not_login':user_not_login, 'user_login':user_login, 'categories':categories}
    return render(request,'app/register.html', context)

# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request,username=username, password=password)
#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:messages.info(request,'user or password  not correct!')
            
#     context = {}
#     return render(request,'app/login.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        context = {
            'user_not_login': 'hidden',
            'user_login': 'show'
        }
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect!')
    categories = Category.objects.filter(is_sub=False)
    context = {
        'user_not_login': 'show', 
        'user_login': 'hidden',
        'categories':categories
    }
    
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')


# def home(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer = customer, complete = False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items
#     else:
#         items = []
#         order ={'get_cart_items':0, 'get_cart_total':0}
#         cartItems = order['get_cart_items']

#     products = Product.objects.all()
#     context= {'products': products, 'cartItems':cartItems}
#     return render(request, 'app/home.html', context)


def home(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            # Handle the case where the customer does not exist for the user
            customer = Customer.objects.create(user=request.user, name=request.user.username, email=request.user.email)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
        
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    products = Product.objects.all()
    context = {
        'categories':categories,
        'active_category':active_category, 
        'products': products, 
        'cartItems': cartItems, 
        'user_not_login':user_not_login, 
        'user_login':user_login
    }
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order ={'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    context = {
        'categories':categories,
        'active_category':active_category,
        'items': items, 
        'order': order, 
        'cartItems':cartItems, 
        'user_not_login':user_not_login, 
        'user_login':user_login
    }
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.method == "POST":
        # Lấy thông tin từ form
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        phone = request.POST.get('phone', '')
        country = request.POST.get('country', '')

        # Cập nhật thông tin khách hàng
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={'name': name, 'email': email}
        )

        if not created:
            customer.name = name
            customer.email = email
            customer.save()

        # Cập nhật hoặc tạo đơn hàng
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # Cập nhật hoặc tạo địa chỉ giao hàng
        shipping_address, created = ShippingAddress.objects.get_or_create(
            customer=customer,
            order=order,
            defaults={
                'address': address,
                'city': city,
                'state': state,
                'mobile': phone
            }
        )

        if not created:
            shipping_address.address = address
            shipping_address.city = city
            shipping_address.state = state
            shipping_address.mobile = phone
            shipping_address.save()

        return redirect('checkout')

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
        
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    
    context = {
        'categories': categories,
        'active_category': active_category,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    
    return render(request, 'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
        
    return JsonResponse('added', safe=False)