from django.test import TestCase
from django.urls import resolve , reverse
from ..views import *
from django.contrib.auth.models import User
from ..models import *
from decimal import Decimal

# index page
class IndexTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username= 'john',
            email= 'john@doe.com',
            password='123')
        self.client.login( username='john' , password='123')

    def test_order_index_resolve(self):
        view = resolve('/1/index/')
        self.assertEquals(view.func, index)

    # testing create_order(views.create_order)
    def test_create_order_redirects(self):
        response = self.client.get('/create_order/')
        self.assertRedirects(response , '/1/menu/')

    def test_order_index_created_order_status_code(self):
        self.client.get('/create_order/')
        url = reverse('index', args=(1,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_order_index_not_created_order_status_code(self):
        url = reverse('index', args=(1,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_order_index_created_order_already_done(self):
        self.client.get('/create_order/')
        response = self.client.get('/create_order/')
        self.assertRedirects(response , '/1/index/')

    # testing destroy_order(views.destroy_order)
    def test_destroy_order_redirect(self):
        self.client.get('/create_order/')
        response = self.client.get('/1/destroy_order/')
        self.assertRedirects(response , '/2/menu/')

    def test_order_index_destroyed_order_status_code(self):
        self.client.get('/create_order/')
        url1 = reverse('index', args=(1,))
        self.client.get('/1/destroy_order/')
        url2 = reverse('index', args=(2,))
        response1 = self.client.get(url1)
        response2 = self.client.get(url2)
        self.assertEquals(response1.status_code, 404) and self.assertEquals(response2.status_code, 200)

    def test_order_index_destroyed_order_no_order_created(self):
        response = self.client.get('/1/destroy_order/')
        self.assertEquals(response.status_code, 404)

    def test_order_index_destroyed_order_different_user(self):
        self.client.get('/create_order/')
        self.client.logout()
        User.objects.create_user(
            username= 'dave',
            email= 'dave@doe.com',
            password='456')
        self.client.login( username='dave' , password='456')
        response = self.client.get('/1/destroy_order/')
        self.assertEquals(response.status_code , 403)

    def test_order_index_destroyed_order_order_already_bought(self):
        self.client.get('/create_order/')
        TemplatePasta.objects.create( name='abc' , SmallPrice = Decimal(1.0))
        self.client.post('/1/1/1/rest/')
        self.client.get('/1/view/')
        response = self.client.get('/1/destroy_order/')
        self.assertEquals(response.status_code , 403)

    # testing template format of index
    def test_order_index_not_found_status_code(self):
        url = reverse('index', args=(99,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_redirection(self):
        login_url = reverse('login')
        self.client.get('/logout/')
        url = reverse(index , args=(1,))
        response = self.client.get(reverse(index , args=(1,)))
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=url))

    def test_forbidden(self):
        self.client.get('/create_order/')
        self.client.get('/logout')
        User.objects.create_user(
            username= 'dave',
            email= 'dave@doe.com',
            password='456')
        self.client.login( username='dave' , password='456')
        response = self.client.get(reverse(index , args=(1,)))
        self.assertEquals(response.status_code , 403)

    def test_item_lists(self):
        self.client.get('/create_order/')
        url = reverse('index', args=(1,))
        response = self.client.get(url)
        items = response.context[-1]
        #print([d.keys() for d in items])
        contains = False
        for item in [d.keys() for d in items]:
            if len(item) == 9:
                contains = True
        self.assertTrue(contains)

    def test_index_view_contains_menu_logout_links_page(self):
        self.client.get('/create_order/')
        response = self.client.get('/1/index/')
        self.assertContains(response, 'href="{0}"'.format('/1/menu/')) and self.assertContains(self.response, 'href="{0}"'.format('/logout/'))

    def test_order_total_destroy_links(self):
        self.client.get('/create_order/')
        TemplatePasta.objects.create( name='abc' , SmallPrice = Decimal(1.0))
        res= self.client.post('/1/1/1/rest/')
        response = self.client.get('/1/index/')
        self.assertContains(response, 'href="{0}"'.format('/1/view/')) and self.assertContains(self.response, 'href="{0}"'.format('/destroy_order/'))

    # testing confirm_order(views.view)
    def test_index_confirm_order(self):
        self.client.get('/create_order/')
        TemplatePasta.objects.create( name='abc' , SmallPrice = Decimal(1.0))
        self.client.post('/1/1/1/rest/')
        self.client.get('/1/index/')
        response = self.client.get('/1/view/')
        self.assertRedirects(response , reverse('home'))

    def test_index_confirm_order_already_bought(self):
        self.client.get('/create_order/')
        TemplatePasta.objects.create( name='abc' , SmallPrice = Decimal(1.0))
        self.client.post('/1/1/1/rest/')
        self.client.get('/1/view/')
        response = self.client.get('/1/view/')
        self.assertEquals(response.status_code , 403)

    def test_index_confirm_order_different_user(self):
        self.client.get('/create_order/')
        TemplatePasta.objects.create( name='abc' , SmallPrice = Decimal(1.0))
        self.client.post('/1/1/1/rest/')
        self.client.get('/1/view/')
        self.client.logout()
        User.objects.create_user(
            username= 'dave',
            email= 'dave@doe.com',
            password='456')
        self.client.login( username='dave' , password='456')
        response = self.client.get('/1/view/')
        self.assertEquals(response.status_code , 403)
