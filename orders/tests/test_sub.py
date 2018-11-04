from django.test import TestCase
from django.urls import resolve , reverse
from ..views import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your tests here.
from ..forms import SignUpForm
from ..models import *
from decimal import Decimal

# sub page
class SubTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username= 'john',
            email= 'john@doe.com',
            password='123')
        self.client.login( username='john' , password='123')
        Order.objects.create( user=user )
        TemplateSub.objects.create( name='abc' )

    def test_order_404(self):
        self.client.get('/1/destroy_order/')
        response = self.client.get('/1/1/sub/')
        self.assertEquals( response.status_code , 404)

    def test_sub_404(self):
        TemplateSub.objects.get(pk=1).delete()
        response = self.client.get('/1/1/sub/')
        self.assertEquals( response.status_code , 404)

    def test_template_exists(self):
        set = TemplateSub.objects.all()
        self.assertEquals( len(set) , 1 )

    def test_sub_exists(self):
        response = self.client.post('/1/1/sub/' , {"size": "Small" , 'Xcheese': 'No'})
        self.assertRedirects(response , '/1/menu/') and self.assertEquals(len(Sub.objects.all()) , 1)

    def test_no_size_forbidden(self):
        response = self.client.post('/1/1/sub/' , {'size': 'NoEntry' , 'Xcheese': 'No'})
        self.assertEquals(response.status_code , 403)
