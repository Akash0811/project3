from django.contrib import admin

from .models import Order , TemplateRegularPizza , TemplateSicilianPizza , TemplateSub , TemplateDinnerPlatter , TemplatePasta , TemplateSalad , Topping , Add_on

# Register your models here.

#admin.site.register(Order)
admin.site.register(TemplateRegularPizza)
admin.site.register(TemplateSicilianPizza)
admin.site.register(TemplateSub)
admin.site.register(TemplateDinnerPlatter)
admin.site.register(TemplatePasta)
admin.site.register(TemplateSalad)
admin.site.register(Topping)
admin.site.register(Add_on)

'''Add order confirmation view in admin.py
override django's changelist_view
'''
@admin.register(Order)
class MyModelAdmin(admin.ModelAdmin):
    change_list_template = 'admin/confirmation.html'
    def changelist_view(self, request, extra_context={}):
        orders = Order.objects.filter( buy = True ).all()
        extra_context['orders'] = orders
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        return response
