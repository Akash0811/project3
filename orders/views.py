from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect , HttpResponseForbidden
from django.shortcuts import render , get_object_or_404 , redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
#from django.core.mail import send_mail
from .forms import SignUpForm

from .models import Order , RegularPizza , SicilianPizza , Sub , DinnerPlatter , Pasta , Salad , Topping , Add_on , Steak_Cheese ,\
                    TemplateRegularPizza , TemplateSicilianPizza , TemplateSub , TemplateDinnerPlatter , TemplatePasta , TemplateSalad

# homepage
class HomeListView(TemplateView):
    template_name = 'orders/home.html'
    def get_context_data(self , *args , **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        context = {
            "RegularPizza": TemplateRegularPizza.objects.all(),
            "SicilianPizza": TemplateSicilianPizza.objects.all(),
            "Sub": TemplateSub.objects.all(),
            "Pasta": TemplatePasta.objects.all(),
            "Salad": TemplateSalad.objects.all(),
            "DinnerPlatter": TemplateDinnerPlatter.objects.all(),
            "Add_on": Add_on.objects.all(),
        }
        return context

# adds item to cart
@login_required
def index(request , order_id):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    order = get_object_or_404(Order , pk = order_id)
    if order.user != request.user or order.buy:
        return HttpResponseForbidden("Forbidden")
    content = {
        "order_id": order.id,
        "regular_pizza": order.regular_dish.all(),
        "sicilian_pizza": order.sicilian_dish.all(),
        "sub": order.subs0_dish.all(),
        "Steak_Cheese": Steak_Cheese.objects.filter( orders=order ) ,
        "pasta": order.pasta_dish.all(),
        "salad": order.salad_dish.all(),
        "dinner_platter": order.din_dish.all(),
        "total": order.price
    }
    return render( request , "orders/index.html" , content  )

# Create your views here.
@method_decorator(login_required, name='dispatch')
class MenuListView(TemplateView):
    template_name = 'orders/menu.html'
    def get(self , *args , **kwargs):
        order = get_object_or_404(Order , pk = self.kwargs['order_id'])
        if order.user != self.request.user or order.buy:
            return HttpResponseForbidden("Forbidden")
        return super(MenuListView , self).get(*args , **kwargs)
    def get_context_data(self , *args , **kwargs):
        order = get_object_or_404(Order , pk = self.kwargs['order_id'])
        context = super(MenuListView, self).get_context_data(**kwargs)
        context = {
            "user": self.request.user,
            "order_id": order.id,
            "RegularPizza": TemplateRegularPizza.objects.all(),
            "SicilianPizza": TemplateSicilianPizza.objects.all(),
            "Sub": TemplateSub.objects.all(),
            "Pasta": TemplatePasta.objects.all(),
            "Salad": TemplateSalad.objects.all(),
            "DinnerPlatter": TemplateDinnerPlatter.objects.all(),
            "Add_on": Add_on.objects.all(),
        }
        return context

# Confirm order
@login_required
def view(request , order_id):
    order = get_object_or_404(Order , pk = order_id)
    if order.user != request.user:
        return HttpResponseForbidden("Forbidden")
    order.buy = True
    order.save()
    '''
    Provide host username and password in settings.py
    Also turn on less_secure_apps functionality on gmail
    '''
    return HttpResponseRedirect(reverse('home'))

# Creates new objects
@login_required
def create_order(request):
    order = Order.objects.filter( user = request.user ).last()
    if not order:
        order = Order.objects.create( user = request.user )
    elif order.buy:
        order = Order.objects.create( user = request.user )
    else:
        return HttpResponseRedirect(reverse("index" , args=(order.id,)))
    return HttpResponseRedirect(reverse("menu" , args=(order.id,)))

# Destroys new objects
@login_required
def destroy_order(request , order_id):
    order = get_object_or_404(Order , pk = order_id)
    if order.user != request.user or order.buy :
        return HttpResponseForbidden("Forbidden")
    order.delete()
    return create_order(request)

# Redirects user to login , doesnot sign him up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'orders/register.html', {'form': form})

# dish_id is special or regular
# order corresponds to which user order
# dish_id is template id

@login_required
def regular_pizza(request , dish_id , order_id ):
    order = get_object_or_404(Order , pk = order_id)
    if order.user != request.user or order.buy:
        return HttpResponseForbidden("Forbidden")
    if request.method == 'GET':
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "Topping": Topping.objects.all()
        }
        return render( request , "orders/regular_pizza.html" , context)
    size = request.POST["size"]
    if size == "NoEntry":
        return HttpResponseForbidden("Please provide size")
    template = get_object_or_404(TemplateRegularPizza , pk = dish_id)
    pizza = RegularPizza.objects.create(orders = order,
                                        template = template)
    count = 0
    string = "Topping(s): "
    for topping in Topping.objects.all():
        if request.POST[topping.name] == 'Yes':
            pizza.toppings.add(topping)
            string += f" {topping.name}"
            count += 1
    pizza.no_of_toppings = count
    if pizza.template.name != 'Special' and count > 3:
        pizza.delete()
        return HttpResponseForbidden("Can only add a maximum of 3 toppings")
    if pizza.template.name == 'Special' and count != 5:
        pizza.delete()
        return HttpResponseForbidden("Special Pizza has 5 toppings")
    pizza.string = string
    if size == "Small":
        order.price += pizza.price()
    else:
        pizza.size = True
        order.price += pizza.price()
    pizza.save()
    order.save()
    return HttpResponseRedirect(reverse("menu", args=(order_id,)))

@login_required
def sicilian_pizza(request , dish_id , order_id ):
    order = get_object_or_404(Order , pk = order_id)
    if order.user != request.user or order.buy:
        return HttpResponseForbidden("Forbidden")
    if request.method == 'GET':
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "Topping": Topping.objects.all()
        }
        return render( request , "orders/sicilian_pizza.html" , context)
    size = request.POST["size"]
    if size == "NoEntry":
        return HttpResponseForbidden("Please provide size")
    template = get_object_or_404(TemplateSicilianPizza , pk = dish_id)
    pizza = SicilianPizza.objects.create(orders = order,
                                         template = template)
    count = 0
    string = "Topping(s): "
    for topping in Topping.objects.all():
        if request.POST[topping.name] == 'Yes':
            pizza.toppings.add(topping)
            string += f" {topping.name}"
            count += 1
    pizza.no_of_toppings = count
    if pizza.template.name != 'Special' and count > 3:
        pizza.delete()
        return HttpResponseForbidden("Can only add a maximum of 3 toppings")
    if pizza.template.name == 'Special' and count != 5:
        pizza.delete()
        return HttpResponseForbidden("Special Pizza has 5 toppings")
    pizza.string = string
    if size == "Small":
        order.price += pizza.price()
    else:
        pizza.size = True
        order.price += pizza.price()
    pizza.save()
    order.save()
    return HttpResponseRedirect(reverse("menu", args=(order_id,)))

@login_required
def sub(request , dish_id , order_id ):
    order = get_object_or_404(Order , pk = order_id)
    if order.user != request.user or order.buy:
        return HttpResponseForbidden("Forbidden")
    if request.method == 'GET':
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "Add_on": Add_on.objects.all()
        }
        return render( request , "orders/sub.html" , context)
    size = request.POST["size"]
    if size == "NoEntry":
        return HttpResponseForbidden("Please provide size")
    Xcheese = request.POST["Xcheese"]
    template = get_object_or_404(TemplateSub , pk = dish_id)

    # Steak Cheese exception
    if dish_id == 10:
        sub = Steak_Cheese.objects.create( orders=order,
                                           template=template)
        count = 0
        string = "Add-on(s): "
        for item in Add_on.objects.all():
            if request.POST[item.name] == 'Yes':
                sub.Add_ons.add(item)
                string += f" {item.name}"
                count += 1
        sub.no_of_add_ons = count
        sub.string = string
    else:
        sub = Sub.objects.create( orders=order,
                                  template=template)

        # Sausage , Peppers & Onions exception
        if sub.template.name == "Sausage , Peppers & Onions" and size == "Small":
            sub.delete()
            return HttpResponseForbidden("Small Size is not Available")
    if Xcheese == "Yes":
        sub.Xcheese = True
    if size == "Small":
        order.price += sub.price()
    else:
        sub.size = True
        order.price += sub.price()
    sub.save()
    order.save()
    return HttpResponseRedirect(reverse("menu", args=(order_id,)))

@login_required
def rest(request , type_id , dish_id , order_id ):
    order = get_object_or_404(Order , pk = order_id)
    if order.user != request.user or order.buy:
        return HttpResponseForbidden("Forbidden")
    if request.method == 'GET':
        context = {
            "order_id": order_id,
            "dish_id": dish_id,
            "type_id": type_id
        }
        return render( request , "orders/rest.html" , context)
    if type_id == 1:
        template = get_object_or_404(TemplatePasta , pk = dish_id)
        pasta = Pasta.objects.create( orders=order,
                                      template=template)
        order.price += pasta.price()
        pasta.save()
    elif type_id == 2:
        template = get_object_or_404(TemplateSalad , pk = dish_id)
        salad = Salad.objects.create( orders=order,
                                      template=template)
        order.price += salad.price()
        salad.save()
    elif type_id == 3:
        template = get_object_or_404(TemplateDinnerPlatter , pk = dish_id)
        dinner = DinnerPlatter.objects.create( orders=order,
                                               template=template)
        order.price += dinner.price()
        dinner.save()
    else:
        template = get_object_or_404(TemplateDinnerPlatter , pk = dish_id)
        dinner = DinnerPlatter.objects.create( size=True,
                                               orders=order,
                                               template=template)
        order.price += dinner.price()
        dinner.save()
    order.save()
    return HttpResponseRedirect(reverse("menu", args=(order_id,)))

@login_required
def confirmed_orders( request ):
    if request.user.is_superuser:
        context = {
            "orders": Order.objects.filter( buy = True ).all()
        }
        return render(request, "orders/confirmed_orders.html", context )
    else:
        logout(request)
        return render(request, "orders/login.html", {"message": "Forbidden"})
