from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .filters import OrderFilter
from .forms import CreateUserForm, OrderForm
from .models import Customer, Order, Product


# Create your views here.
# @login_required(login_url='Accounts:LoginPage')
# @allowed_users(allowed_roles=['admin'])
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    deliverd = orders.filter(status = 'Deliverd').count()
    panding = orders.filter(status ='Pending').count()
    context = {
        "customers" : customers,
        'orders' : orders,
        'total_customers' : total_customers,
        'total_orders' : total_orders,
        'deliverd' : deliverd,
        'panding' : panding
    }
    return render(request,"dashboard.html",context)

# @login_required(login_url='Accounts:LoginPage')
# @allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    context = {
       "products" : products
    }
    return render(request,"products.html",context)

# @login_required(login_url='Accounts:LoginPage')
def customer(request,id):
    customers = Customer.objects.get(id=id)
    orders = customers.order_set.all()
    myfilter = OrderFilter(request.GET,queryset=orders)
    orders = myfilter.qs
    order_count = orders.count()
    context = {
        "customers" : customers,
        'orders': orders,
        'order_count' : order_count,
        'myfilter' : myfilter
    }
    return render(request,"customers.html",context)

# @login_required(login_url='Accounts:LoginPage')
def create_order(request,id):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer = Customer.objects.get(id=id)
    form = OrderForm(initial={'customer' : customer})
    fromset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        fromset = OrderFormSet(request.POST,instance=customer)
        if fromset.is_valid():
            fromset.save()
            return redirect("Accounts:home")
    context = {
        'fromset' : fromset
    }
    return render(request,'order_form.html',context)

# @login_required(login_url='Accounts:LoginPage')
def update_order(request,id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect("Accounts:home")
    context = {
        'form' : form
    }

    return render(request,'order_form.html',context)

# @login_required(login_url='Accounts:LoginPage')
def delete_order(request,id):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect("Accounts:home")


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'account was created for  ' + user)
            return redirect("Accounts:LoginPage")
    context = {
        'form' : form
        }
    return render(request,'register.html',context)

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password = password)
        if user is not None :
            login(request,user)
            return redirect("Accounts:home")
        else :
            messages.info(request,"Username or password is incorrect")
    context = {}
    return render(request,'login.html',context)

def LogoutUser(request):
    logout(request)
    return redirect("Accounts:LoginPage")

