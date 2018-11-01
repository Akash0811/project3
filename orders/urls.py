from django.urls import path
from django.contrib.auth import views as auth_views

from orders import views

urlpatterns = [
    path("", views.HomeListView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='orders/login.html'), name='login'),
    path("<int:order_id>/index/", views.index, name="index"),
    path("create_order/", views.create_order , name="create_order"),
    path("<int:order_id>/destroy_order/", views.destroy_order , name="destroy_order"),
    path("register/", views.signup, name="register"),
    path('logout/', auth_views.LogoutView.as_view(template_name='orders/login.html'), name='logout'),
    path("<int:order_id>/menu/", views.MenuListView.as_view(), name="menu"),
    path("<int:order_id>/<int:dish_id>/<int:type_id>/rest/", views.rest, name="rest"),
    path("<int:order_id>/<int:dish_id>/sub/", views.sub, name="sub"),
    path("<int:order_id>/<int:dish_id>/regular_pizza/", views.regular_pizza, name="regular_pizza"),
    path("<int:order_id>/<int:dish_id>/sicilian_pizza/", views.sicilian_pizza, name="sicilian_pizza"),
    path("<int:order_id>/view/", views.view, name="view"),
    path("confirmed_orders/", views.confirmed_orders, name="confirmed_orders"),
]
