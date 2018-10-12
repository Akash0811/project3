from django.urls import path
from django.contrib.auth import views as auth_views

from orders import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("<int:order_id>/index/", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.signup, name="register"),
    path('logout/', auth_views.LogoutView.as_view(template_name='orders/login.html'), name='logout'),
    path("<int:order_id>/menu/", views.menu, name="menu"),
    path("<int:order_id>/<int:dish_id>/<int:type_id>/rest/", views.rest, name="rest"),
    path("<int:order_id>/<int:dish_id>/sub/", views.sub, name="sub"),
    path("<int:order_id>/<int:dish_id>/regular_pizza/", views.regular_pizza, name="regular_pizza"),
    path("<int:order_id>/<int:dish_id>/sicilian_pizza/", views.sicilian_pizza, name="sicilian_pizza"),
    path("<int:order_id>/view/", views.view, name="view"),
    path("confirmed_orders/", views.confirmed_orders, name="confirmed_orders"),
]
