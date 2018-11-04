from django.test import TestCase
from django.urls import resolve , reverse
from ..views import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your tests here.
from ..forms import SignUpForm
from ..models import *
from decimal import Decimal

# menu page
class MenuTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username= 'john',
            email= 'john@doe.com',
            password='123')
        self.client.login( username='john' , password='123')

    def test_menu_view_status_code(self):
        response = self.client.get('/1/menu/')
        self.assertEquals(response.status_code, 404)

    def test_menu_url_resolves_home_view(self):
        self.client.get('/create_order/')
        view = resolve('/1/menu/')
        self.assertEquals(view.func.view_class, MenuListView)

    def test_menu_view_contains_index_logout_links_page(self):
        self.client.get('/create_order/')
        response = self.client.get('/1/menu/')
        self.assertContains(response, 'href="{0}"'.format('/1/index/')) and self.assertContains(response, 'href="{0}"'.format('/logout/'))

    '''views.py has 9 contextual keys in
    MenuListView's last context
    '''
    def test_item_lists(self):
        self.client.get('/create_order/')
        url = reverse('menu' , args=(1,))
        response = self.client.get(url)
        items = response.context[-1]
        #print([d.keys() for d in items])
        contains = False
        for item in [d.keys() for d in items]:
            if len(item) == 9:
                contains = True
        self.assertTrue(contains)
