from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey( User , on_delete=models.CASCADE )
    price = models.FloatField( default = 0.0 )
    buy = models.BooleanField( default = False)
    time = now()

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

class SizableDish(NonSizableDish):
    LargePrice = models.FloatField(null=True, blank=True, default=None)
    size = models.BooleanField(default = False)

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
class RegularPizza(TemplateRegularPizza):
    orders = models.ManyToManyField(Order, null = True , blank=True, related_name="regular_dish")
    #toppings = models.ManyToManyField(Topping, null = True , blank=True, related_name="reg_dish")
    no_of_toppings = models.IntegerField( default = 0 )

    def price(self):
        if self.size == False:
            if self.no_of_toppings == 1:
                return self.Topping1SmallPrice
            elif self.no_of_toppings == 2:
                return self.Topping2SmallPrice
            elif self.no_of_toppings == 3:
                return self.Topping3SmallPrice
            else:
                return self.SmallPrice
        else:
            if self.no_of_toppings == 1:
                return self.Topping1LargePrice
            elif self.no_of_toppings == 2:
                return self.Topping2LargePrice
            elif self.no_of_toppings == 3:
                return self.Topping3LargePrice
            else:
                return self.LargePrice


class SicilianPizza(TemplateSicilianPizza):
    orders = models.ManyToManyField(Order, null = True , blank=True, related_name="sicilian_dish")
    #toppings = models.ManyToManyField(Topping, blank=True, related_name="sic_dish")
    no_of_toppings = models.IntegerField( default = 0 )

    def price(self):
        if self.size == False:
            if self.no_of_toppings == 1:
                return self.Topping1SmallPrice
            elif self.no_of_toppings == 2:
                return self.Topping2SmallPrice
            elif self.no_of_toppings == 3:
                return self.Topping3SmallPrice
            else:
                return self.SmallPrice
        else:
            if self.no_of_toppings == 1:
                return self.Topping1LargePrice
            elif self.no_of_toppings == 2:
                return self.Topping2LargePrice
            elif self.no_of_toppings == 3:
                return self.Topping3LargePrice
            else:
                return self.LargePrice

class Sub(TemplateSub):
    orders = models.ManyToManyField(Order, null = True , blank=True, related_name="subs0_dish")
    Xcheese = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.name} - Small:{self.SmallPrice} - Large:{self.LargePrice} - ExtraCheese:{self.XCheesePrice}"

    def price(self):
        if self.size == False:
            if self.Xcheese == False:
                return self.SmallPrice
            else:
                return self.SmallPrice + self.XCheesePrice
        else:
            if self.Xcheese == False:
                return self.LargePrice
            else:
                return self.LargePrice + self.XCheesePrice

class DinnerPlatter(TemplateDinnerPlatter):
    orders = models.ManyToManyField(Order, null = True , blank=True, related_name="din_dish")

    def price(self):
        return self.SmallPrice

class Pasta(TemplatePasta):
    orders = models.ManyToManyField(Order, null = True , blank=True, related_name="pasta_dish")

    def price(self):
        return self.SmallPrice

class Salad(TemplateSalad):
    orders = models.ManyToManyField(Order, null = True , blank=True, related_name="salad_dish")

    def price(self):
        return self.SmallPrice
