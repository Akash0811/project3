from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("", views.cart, name="cart"),
    path("rest", views.rest, name="rest"),
    path("sub", views.sub, name="sub"),
    path("regular_pizza", views.regular_pizza, name="regular_pizza"),
    path("sicilian_pizza", views.sicilian_pizza, name="sicilian_pizza")
]
