from django.test import TestCase
from django.urls import resolve , reverse
from ..views import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your tests here.
from ..forms import SignUpForm
from ..models import *
from decimal import Decimal

# home page
class HomeTests(TestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, HomeListView)

    def test_home_view_contains_login_register_links_page(self):
        self.assertContains(self.response, 'href="{0}"'.format('/login/')) and self.assertContains(self.response, 'href="{0}"'.format('/register/'))

    def test_home_view_contains_create_logout_links_page(self):
        User.objects.create_user(
            username= 'john',
            email= 'john@doe.com',
            password='123')
        self.client.login( username='john' , password='123')
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'href="{0}"'.format('/create_order/')) and self.assertContains(response, 'href="{0}"'.format('/logout/'))

    '''views.py has 7 contextual keys in
    HomeListView's last context
    '''
    def test_item_lists(self):
        url = reverse('home')
        response = self.client.get(url)
        items = response.context[-1]
        #print([d.keys() for d in items])
        contains = False
        for item in [d.keys() for d in items]:
            if len(item) == 7:
                contains = True
        self.assertTrue(contains)
