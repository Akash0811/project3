from django.contrib import admin

from .models import Order , RegularPizza , SicilianPizza , Sub , DinnerPlatter , Pasta , Salad , Topping

# Register your models here.


admin.site.register(Order)
admin.site.register(RegularPizza)
admin.site.register(SicilianPizza)
admin.site.register(Sub)
admin.site.register(DinnerPlatter)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Topping)
