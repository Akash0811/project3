from django.test import TestCase
from django.urls import resolve , reverse
from ..views import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your tests here.
from ..forms import SignUpForm
from ..models import *
from decimal import Decimal

# regular_pizza page
class RegularPizzaTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username= 'john',
            email= 'john@doe.com',
            password='123')
        self.client.login( username='john' , password='123')
        Order.objects.create( user=user )
        TemplateRegularPizza.objects.create( name='abc' )

    def test_order_404(self):
        self.client.get('/1/destroy_order/')
        response = self.client.get('/1/1/regular_pizza/')
        self.assertEquals( response.status_code , 404)

    def test_pizza_404(self):
        x = TemplateRegularPizza.objects.filter(pk=1).delete()
        response = self.client.get('/1/1/regular_pizza/')
        self.assertEquals( response.status_code , 404)

    def test_template_exists(self):
        set = TemplateRegularPizza.objects.all()
        self.assertEquals( len(set) , 1 )

    def test_regular_pizza_exists(self):
        response = self.client.post('/1/1/regular_pizza/' , {"size": "Small"})
        self.assertRedirects(response , '/1/menu/') and self.assertEquals(len(RegularPizza.objects.all()) , 1)

    # topping model works
    def test_3_toppings_pizza_exists(self):
        Topping.objects.create( name="a")
        Topping.objects.create( name="b")
        Topping.objects.create( name="c")
        response = self.client.post('/1/1/regular_pizza/' ,{'size': 'Small' , 'a':'Yes' , 'b':'Yes' , 'c':'Yes' })
        self.assertRedirects(response , '/1/menu/')

    def test_no_size_forbidden(self):
        response = self.client.post('/1/1/regular_pizza/' , {'size': 'NoEntry'})
        self.assertEquals(response.status_code , 403)

    def test_more_than_3_toppings_size_forbidden(self):
        Topping.objects.create( name="a")
        Topping.objects.create( name="b")
        Topping.objects.create( name="c")
        Topping.objects.create( name="d")
        response = self.client.post('/1/1/regular_pizza/' ,{'size': 'Small' , 'a':'Yes' , 'b':'Yes' , 'c':'Yes' , 'd':'Yes' })
        self.assertEquals(response.status_code , 403)

    # Special pizza
    def test_special_5_toppings_exists(self):
        Topping.objects.create( name="a")
        Topping.objects.create( name="b")
        Topping.objects.create( name="c")
        Topping.objects.create( name="d")
        Topping.objects.create( name="e")
        TemplateRegularPizza.objects.create( name='Special' )
        response = self.client.post('/1/2/regular_pizza/' ,{'size': 'Small' , 'a':'Yes' , 'b':'Yes' , 'c':'Yes' , 'd':'Yes' , 'e':'Yes' })
        self.assertRedirects(response , '/1/menu/')

    def test_special_3_toppings_forbidden(self):
        Topping.objects.create( name="a")
        Topping.objects.create( name="b")
        Topping.objects.create( name="c")
        TemplateRegularPizza.objects.create( name='Special' )
        response = self.client.post('/1/2/regular_pizza/' ,{'size': 'Small' , 'a':'Yes' , 'b':'Yes' , 'c':'Yes' })
        self.assertEquals(response.status_code , 403)

    def test_special_6_toppings_forbidden(self):
        Topping.objects.create( name="a")
        Topping.objects.create( name="b")
        Topping.objects.create( name="c")
        Topping.objects.create( name="d")
        Topping.objects.create( name="e")
        Topping.objects.create( name="f")
        TemplateRegularPizza.objects.create( name='Special' )
        response = self.client.post('/1/2/regular_pizza/' ,{'size': 'Small' , 'a':'Yes' , 'b':'Yes' , 'c':'Yes' , 'd':'Yes' , 'e':'Yes' , 'f':'Yes'})
        self.assertEquals(response.status_code , 403)
