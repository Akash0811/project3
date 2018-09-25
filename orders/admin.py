from django.contrib import admin

from .models import Order , TemplateRegularPizza , TemplateSicilianPizza , TemplateSub , TemplateDinnerPlatter , TemplatePasta , TemplateSalad , Topping

# Register your models here.

admin.site.register(Order)
admin.site.register(TemplateRegularPizza)
admin.site.register(TemplateSicilianPizza)
admin.site.register(TemplateSub)
admin.site.register(TemplateDinnerPlatter)
admin.site.register(TemplatePasta)
admin.site.register(TemplateSalad)
admin.site.register(Topping)
