from django.db import models
from django.utils.timezone import now

# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=64 , default = "MyOrder")
    time = now()
    pass

class NonSizableDish(models.Model):
    name = models.CharField(max_length=64)
    #orders = models.ManyToManyField(Order, blank=True, related_name="dish")
    SmallPrice = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name} - {self.SmallPrice}"

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class SmallSize(models.Model):
    name = models.CharField(max_length=64)
    big = models.BooleanField(default=False)

class ExtraCheese(models.Model):
    extra = models.BooleanField(default=False)

class SizableDish(NonSizableDish):
    LargePrice = models.FloatField(null=True, blank=True, default=None)
    size = models.ManyToManyField(SmallSize, blank=True, related_name="dish")

    def __str__(self):
        return f"{self.name} - Small:{self.SmallPrice} - Large:{self.LargePrice}"

'''templates contain pice of items to be shown on menu
Admin can change prices dynamically
Required because cannot have same database for templates and orders'''

class TemplateRegularPizza(SizableDish):
    Topping1SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping2SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping3SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping1LargePrice = models.FloatField(null=True, blank=True, default=None)
    Topping2LargePrice = models.FloatField(null=True, blank=True, default=None)
    Topping3LargePrice = models.FloatField(null=True, blank=True, default=None)

class TemplateSicilianPizza(SizableDish):
    Topping1SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping2SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping3SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping1LargePrice = models.FloatField(null=True, blank=True, default=None)
    Topping2LargePrice = models.FloatField(null=True, blank=True, default=None)
    Topping3LargePrice = models.FloatField(null=True, blank=True, default=None)

class TemplateSub(SizableDish):
    XCheesePrice = models.FloatField(null=True, blank=True, default=0.50)

    def __str__(self):
        return f"{self.name} - Small:{self.SmallPrice} - Large:{self.LargePrice} - ExtraCheese:{self.XCheesePrice}"

class TemplateDinnerPlatter(SizableDish):
    pass

class TemplatePasta(NonSizableDish):
    pass

class TemplateSalad(NonSizableDish):
    pass

'''Real orders are passed and hence these are linked to attributes and orders databases
This is displayed on cart , not on menu
'''
class RegularPizza(SizableDish):
    orders = models.ManyToManyField(Order, blank=True, related_name="regular_dish")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="reg_dish")
    no_of_toppings = models.IntegerField( default = 0 )


class SicilianPizza(SizableDish):
    orders = models.ManyToManyField(Order, blank=True, related_name="sicilian_dish")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="sic_dish")
    no_of_toppings = models.IntegerField( default = 0 )


class Sub(SizableDish):
    orders = models.ManyToManyField(Order, blank=True, related_name="subs0_dish")
    Xcheese = models.ManyToManyField(ExtraCheese , related_name = "subs_dish")

    def __str__(self):
        return f"{self.name} - Small:{self.SmallPrice} - Large:{self.LargePrice} - ExtraCheese:{self.XCheesePrice}"

class DinnerPlatter(SizableDish):
    orders = models.ManyToManyField(Order, blank=True, related_name="din_dish")
    pass

class Pasta(NonSizableDish):
    orders = models.ManyToManyField(Order, blank=True, related_name="pasta_dish")
    pass

class Salad(NonSizableDish):
    orders = models.ManyToManyField(Order, blank=True, related_name="salad_dish")
    pass
