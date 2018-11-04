from django.test import TestCase
from django.urls import resolve , reverse
from ..views import *
from django.contrib.auth.models import User
from ..models import *
from decimal import Decimal

# sub page
class RestTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username= 'john',
            email= 'john@doe.com',
            password='123')
        self.client.login( username='john' , password='123')
        Order.objects.create( user=user )
        TemplatePasta.objects.create( name='abc1' )
        TemplateDinnerPlatter.objects.create( name='abc2' )
        TemplateSalad.objects.create( name='abc3' )

    def test_order_404(self):
        self.client.get('/1/destroy_order/')
        response = self.client.get('/1/1/1/rest/')
        self.assertEquals( response.status_code , 404)

    def test_pasta_404(self):
        TemplatePasta.objects.get(pk=1).delete()
        response = self.client.get('/1/1/1/rest/')
        self.assertEquals( response.status_code , 404)

    def test_salad_404(self):
        TemplateSalad.objects.get(pk=1).delete()
        response = self.client.get('/1/1/2/rest/')
        self.assertEquals( response.status_code , 404)

    def test_dinner_platter_404(self):
        TemplateDinnerPlatter.objects.get(pk=1).delete()
        response1 = self.client.get('/1/1/3/rest/')
        response2 = self.client.get('/1/1/4/rest/')
        self.assertEquals( response1.status_code , 404) and self.assertEquals( response2.status_code , 404)

    def test_template_exists(self):
        set1 = TemplatePasta.objects.all()
        set2 = TemplateSalad.objects.all()
        set3 = TemplateDinnerPlatter.objects.all()
        self.assertEquals( len(set1)*len(set2)*len(set3) , 1 )

    def test_pasta_exists(self):
        response = self.client.post('/1/1/1/rest/')
        self.assertRedirects(response , '/1/menu/') and self.assertEquals( len(Pasta.objects.all()) , 1)

    def test_salad_exists(self):
        response = self.client.post('/1/1/2/rest/')
        self.assertRedirects(response , '/1/menu/') and self.assertEquals( len(Salad.objects.all()) , 1)

    def test_dinner_platter_exists(self):
        response1 = self.client.post('/1/1/3/rest/')
        response2 = self.client.post('/1/1/4/rest/')
        self.assertRedirects(response1 , '/1/menu/') and self.assertRedirects(response2 , '/1/menu/') and self.assertEquals( len(DinnerPlatter.objects.all()) , 1)

    def test_reverse_works(self):
        response1 = self.client.get(reverse('rest' , args=(1,1,1)))
        response2 = self.client.get(reverse('rest' , args=(1,1,2)))
        response3 = self.client.get(reverse('rest' , args=(1,1,3)))
        response4 = self.client.get(reverse('rest' , args=(1,1,4)))
        self.assertEquals(response1.status_code , 200) and self.assertEquals(response2.status_code , 200) and self.assertEquals(response3.status_code , 200) and self.assertEquals(response4.status_code , 200)

    def test_type_id_not_feasible(self):
        response = self.client.get('/1/1/99/rest/')
        self.assertEquals(response.status_code , 404)
