from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Order , RegularPizza , SicilianPizza , Sub , DinnerPlatter , Pasta , Salad , Topping ,\
                    TemplateRegularPizza , TemplateSicilianPizza , TemplateSub , TemplateDinnerPlatter , TemplatePasta , TemplateSalad

# Create your views here.
@login_required
def index(request , order_id):
    context = {
        "user": request.user,
        "order_id": order.id,
        "RegularPizza": TemplateRegularPizza.objects.all(),
        "SicilianPizza": TemplateSicilianPizza.objects.all(),
        "Topping": Topping.objects.all(),
        "Sub": TemplateSub.objects.all(),
        "Pasta": TemplatePasta.objects.all(),
        "Salad": TemplateSalad.objects.all(),
        "DinnerPlatter": TemplateDinnerPlatter.objects.all()
    }
    return render(request, "orders/index.html", context)

def login_view(request):
    if request.method == 'GET':
        return render(request, "orders/login.html")
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("cart"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def register(request):
    logout(request)
    if request.method == 'GET':
        return render(request, "orders/register.html")
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    if not username or not password or not email or not first_name or not last_name:
        return render(request, "orders/register.html", {"message": "Please fill Entire Form"})
    elif request.POST["password"] != request.POST["confirm_password"]:
        return render(request, "orders/register.html", {"message": "Passwords Mismatched"})
    user = User.objects.create_user(username , email , password )
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    if user is not None:
        return render(request, "orders/login.html", {"message": None})
    else:
        return render(request, "orders/register.html", {"message": "Please fill Entire Form"})

# dish_id is special or regular
# order corresponds to which user order
@login_required
def regular_pizza(request , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET':
        return render(request, "orders/index.html" , order_id = order_id)
    size = request.POST["size"]
    if size == "Small":
        toppings = request.POST["topping"]
        template = TemplateRegularPizza.objects.get( pk = dish_id )
        pizza = RegularPizza.objects.create( name = template.name )
        pizza.no_of_toppings = len( request.method("topping") )
        pizza.orders = order
        order.price += pizza.price()
        pizza.save()
        return render(request , "orders/index.html", order_id = order_id)
    else:
        toppings = request.POST["topping"]
        template = TemplateRegularPizza.objects.get( pk = dish_id )
        pizza = RegularPizza.objects.create( name = template.name )
        pizza.size = True
        pizza.no_of_toppings = len( request.method("topping") )
        pizza.orders = order
        order.price += pizza.price()
        pizza.save()
        return render(request , "orders/index.html", order_id = order_id)

@login_required
def sicilian_pizza(request , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET':
        return render(request, "orders/index.html")
    size = request.POST["size"]
    if size == "Small":
        toppings = request.POST["topping"]
        template = TemplateSicilianPizza.objects.get( pk = dish_id )
        pizza = SicilianPizza.objects.create( name = template.name )
        pizza.no_of_toppings = len( request.method("topping") )
        pizza.orders = order
        pizza.price += pizza.price()
        pizza.save()
        return render(request , "orders/index.html", order_id = order_id)
    else:
        toppings = request.POST["topping"]
        template = TemplateSicilianPizza.objects.get( pk = dish_id )
        pizza = SicilianPizza.objects.create( name = template.name )
        pizza.size = True
        pizza.no_of_toppings = len( request.method("topping") )
        pizza.orders = order
        order.price += pizza.price()
        pizza.save()
        return render(request , "orders/index.html", order_id = order_id)

@login_required
def sub(request , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET':
        return render(request, "orders/index.html", order_id = order_id)
    size = request.POST["size"]
    if size == "Small":
        template = TemplateSub.objects.get( pk = dish_id )
        sub = Sub.objects.create( name = template.name )
        sub.orders = order
        order.price += sub.price()
        sub.save()
        return render(request , "orders/index.html", order_id = order_id)
    else:
        template = TemplateSub.objects.get( pk = dish_id )
        sub = Sub.objects.create( name = template.name )
        sub.size = True
        sub.orders = order
        order.price += sub.price()
        sub.save()
        return render(request , "orders/index.html", order_id = order_id)

@login_required
def rest(request , type_id , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET':
        return render(request, "orders/index.html", order_id = order_id)
    if type_id ==1:
        template = TemplatePasta.objects.get( pk = dish_id )
        pasta = Pasta.objects.create( name = template.name )
        pasta.orders = order
        order.price += pasta.price()
        pasta.save()
        return render(request , "orders/index.html", order_id = order_id)
    elif type_id ==2:
        template = TemplateSalad.objects.get( pk = dish_id )
        salad = Salad.objects.create( name = template.name )
        salad.orders = order
        order.price += salad.price()
        salad.save()
        return render(request , "orders/index.html", order_id = order_id)
    else:
        template = TemplateDinnerPlatter.objects.get( pk = dish_id )
        dinner = DinnerPlatter.objects.create( name = template.name )
        dinner.orders = order
        order.price += dinner.price()
        dinner.save()
        return render(request , "orders/index.html", order_id = order_id)

# adds item to cart
def cart(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    order = Order.objects.filter( user = request.user ).last()
    if not order:
        order = Order.objects.create( user = request.user )
        order.save()
        content = { "order_id": order.id }
        return render( request , "orders/cart.html" , content )
    elif order.buy:
        order = Order.objects.create( user = request.user )
        order.save()
        content = { "order_id": order.id }
        return render( request , "orders/cart.html" , content )
    else:
        content = {
            "order_id": order.id,
            "regular_pizza": order.regular_dish.all(),
            "sicilian_pizza": order.sicilian_dish.all(),
            "sub": order.subs0_dish.all(),
            "pasta": order.pasta_dish.all(),
            "salad": order.salad_dish.all(),
            "dinner_platter": order.din_dish.all(),
            "total": order.price
        }
        return render( request , "orders/cart.html" , content )

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})
