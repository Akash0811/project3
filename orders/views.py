from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Order , RegularPizza , SicilianPizza , Sub , DinnerPlatter , Pasta , Salad , Topping ,\
                    TemplateRegularPizza , TemplateSicilianPizza , TemplateSub , TemplateDinnerPlatter , TemplatePasta , TemplateSalad,\
                    SizableDish , NonSizableDish

# adds item to cart
def index(request , order_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    order = Order.objects.get(pk = order_id)
    content = {
        "order_id": order.id,
        "regular_pizza": order.regular_dish.all(),
        "sicilian_pizza": order.sicilian_dish.all(),
        "sub": order.subs0_dish.all(),
        "pasta": order.pasta_dish.all(),
        "salad": order.salad_dish.all(),
        "dinner_platter": order.din_dish.all(),
        "total": float("{0:.2f}".format(order.price))
    }
    return render( request , "orders/index.html" , content  )

# Create your views here.
def menu(request , order_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    order = Order.objects.get(pk = order_id)
    context = {
        "user": request.user,
        "order_id": order.id,
        "RegularPizza": TemplateRegularPizza.objects.all()[:2],
        "SicilianPizza": TemplateSicilianPizza.objects.all()[:2],
        "Sub": TemplateSub.objects.all()[:18],
        "Pasta": TemplatePasta.objects.all()[:3],
        "Salad": TemplateSalad.objects.all()[:4],
        "DinnerPlatter": TemplateDinnerPlatter.objects.all()[:6]
    }
    return render(request, "orders/menu.html", context)

def login_view(request):
    if request.method == 'GET':
        return render(request, "orders/login.html")
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        order = Order.objects.filter( user = request.user ).last()
        if not order:
            order = Order.objects.create( user = request.user )
        elif order.buy:
            order = Order.objects.create( user = request.user )
        return HttpResponseRedirect(reverse("index", args=(order.id,)))
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
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "Topping": Topping.objects.all()
        }
        return render( request , "orders/regular_pizza.html" , context)
    size = request.POST["size"]
    template = TemplateRegularPizza.objects.get( pk = dish_id )
    pizza = RegularPizza.objects.create( name = template.name ,
                                        SmallPrice = template.SmallPrice,
                                        LargePrice = template.LargePrice,
                                        Topping1SmallPrice = template.Topping1SmallPrice,
                                        Topping2SmallPrice = template.Topping2SmallPrice,
                                        Topping3SmallPrice = template.Topping3SmallPrice,
                                        Topping1LargePrice = template.Topping1LargePrice,
                                        Topping2LargePrice = template.Topping2LargePrice,
                                        Topping3LargePrice = template.Topping3LargePrice)
    count = 0
    for topping in Topping.objects.all():
        #print(request.POST[topping.name])
        if request.POST[topping.name] == 'Yes':
            count += 1
    pizza.no_of_toppings = count
    pizza.orders.add(order)
    if size == "Small":
        order.price += pizza.price()
        pizza.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    else:
        pizza.size = True
        order.price += pizza.price()
        pizza.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))

@login_required
def sicilian_pizza(request , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET':
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "Topping": Topping.objects.all()
        }
        return render( request , "orders/sicilian_pizza.html" , context)
    size = request.POST["size"]
    template = TemplateSicilianPizza.objects.get( pk = dish_id )
    pizza = SicilianPizza.objects.create( name = template.name ,
                                        SmallPrice = template.SmallPrice,
                                        LargePrice = template.LargePrice,
                                        Topping1SmallPrice = template.Topping1SmallPrice,
                                        Topping2SmallPrice = template.Topping2SmallPrice,
                                        Topping3SmallPrice = template.Topping3SmallPrice,
                                        Topping1LargePrice = template.Topping1LargePrice,
                                        Topping2LargePrice = template.Topping2LargePrice,
                                        Topping3LargePrice = template.Topping3LargePrice)
    count = 0
    for topping in Topping.objects.all():
        #print(request.POST[topping.name])
        if request.POST[topping.name] == 'Yes':
            count += 1
    pizza.no_of_toppings = count
    pizza.orders.add(order)
    if size == "Small":
        order.price += pizza.price()
        pizza.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    else:
        pizza.size = True
        order.price += pizza.price()
        pizza.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))

@login_required
def sub(request , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET':
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
        }
        return render( request , "orders/sub.html" , context)
    size = request.POST["size"]
    Xcheese = request.POST["Xcheese"]
    template = TemplateSub.objects.get( pk = dish_id )
    sub = Sub.objects.create( name = template.name,
                            SmallPrice = template.SmallPrice,
                            LargePrice = template.LargePrice,
                            XCheesePrice = template.XCheesePrice)
    sub.orders.add(order)
    if Xcheese == "Yes":
        sub.Xcheese = True
    if size == "Small":
        order.price += sub.price()
        sub.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    else:
        sub.size = True
        order.price += sub.price()
        sub.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))

@login_required
def rest(request , type_id , dish_id , order_id ):
    order = Order.objects.get( pk = order_id )
    if request.method == 'GET':
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "type_id": type_id
        }
        return render( request , "orders/rest.html" , context)
    if type_id ==1:
        template = TemplatePasta.objects.get( pk = dish_id )
        pasta = Pasta.objects.create( name = template.name,
                                    SmallPrice = template.SmallPrice)
        pasta.orders.add(order)
        order.price += pasta.price()
        pasta.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    elif type_id ==2:
        template = TemplateSalad.objects.get( pk = dish_id )
        salad = Salad.objects.create( name = template.name ,
                                    SmallPrice = template.SmallPrice)
        salad.orders.add(order)
        order.price += salad.price()
        salad.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    elif type_id == 3:
        template = TemplateDinnerPlatter.objects.get( pk = dish_id )
        dinner = DinnerPlatter.objects.create( name = template.name,
                                                SmallPrice = template.SmallPrice,
                                                LargePrice = template.LargePrice)
        dinner.orders.add(order)
        order.price += dinner.price()
        dinner.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))
    else:
        template = TemplateDinnerPlatter.objects.get( pk = dish_id )
        dinner = DinnerPlatter.objects.create( name = template.name,
                                                SmallPrice = template.SmallPrice,
                                                LargePrice = template.LargePrice)
        dinner.size = True
        dinner.orders.add(order)
        order.price += dinner.price()
        dinner.save()
        order.save()
        return HttpResponseRedirect(reverse("menu", args=(order_id,)))

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})
