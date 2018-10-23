from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey( User , on_delete=models.CASCADE )
    price = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    buy = models.BooleanField( default = False)
    time = now()

# Price Abstraction
class NonSizableDish(models.Model):
    name = models.CharField(max_length=64)
    SmallPrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} - {self.SmallPrice}"

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class SizableDish(NonSizableDish):
    LargePrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} - Small:{self.SmallPrice} - Large:{self.LargePrice}"

'''templates contain pice of items to be shown on menu
Admin can change prices dynamically
Required because cannot have same database for templates and orders'''

class TemplateRegularPizza(SizableDish):
    Topping1SmallPrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    Topping2SmallPrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    Topping3SmallPrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    Topping1LargePrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    Topping2LargePrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    Topping3LargePrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )

class TemplateSicilianPizza(SizableDish):
    Topping1SmallPrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    Topping2SmallPrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    Topping3SmallPrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    Topping1LargePrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    Topping2LargePrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )
    Topping3LargePrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.0) )

class TemplateSub(SizableDish):
    XCheesePrice = models.DecimalField( max_digits=7 , decimal_places=2 , default = Decimal(0.50) )

    def __str__(self):
        if self.name == "Sausage , Peppers & Onions":
            return f"{self.name} - Large:{self.LargePrice} - ExtraCheese:{self.XCheesePrice}"
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
class RegularPizza(models.Model):
    size = models.BooleanField(default = False)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE  ,related_name="regular_dish")
    template = models.ForeignKey(TemplateRegularPizza , on_delete=models.CASCADE , related_name="dish")
    toppings = models.ManyToManyField(Topping , blank=True, related_name="reg_dish")
    no_of_toppings = models.IntegerField( default = 0 )
    string = models.CharField( null = True , blank=True , max_length=64 )

    def __str__(self):
        if self.size == True:
            return f"{self.template.name} - Size:Large - {self.string} - {self.price()}"
        return f"{self.template.name} - Size:Small - {self.string} - {self.price()}"

    def price(self):
        template = self.template
        count = self.no_of_toppings
        if self.size == False:
            if count == 1:
                return template.Topping1SmallPrice
            elif count == 2:
                return template.Topping2SmallPrice
            elif count == 3:
                return template.Topping3SmallPrice
            else:
                return template.SmallPrice
        else:
            if count == 1:
                return template.Topping1LargePrice
            elif count == 2:
                return template.Topping2LargePrice
            elif count == 3:
                return template.Topping3LargePrice
            else:
                return template.LargePrice


class SicilianPizza(models.Model):
    size = models.BooleanField(default = False)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE , related_name="sicilian_dish")
    template = models.ForeignKey(TemplateSicilianPizza , on_delete=models.CASCADE , related_name="dish")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="sic_dish")
    no_of_toppings = models.IntegerField( default = 0 )
    string = models.CharField( null = True , blank = True ,max_length=64 )

    def __str__(self):
        if self.size == True:
            return f"{self.template.name} - Size:Large - {self.string} - {self.price()}"
        return f"{self.template.name} - Size:Small - {self.string} - {self.price()}"

    def price(self):
        template = self.template
        count = self.no_of_toppings
        if self.size == False:
            if count == 1:
                return template.Topping1SmallPrice
            elif count == 2:
                return template.Topping2SmallPrice
            elif count == 3:
                return template.Topping3SmallPrice
            else:
                return template.SmallPrice
        else:
            if count == 1:
                return template.Topping1LargePrice
            elif count == 2:
                return template.Topping2LargePrice
            elif count == 3:
                return template.Topping3LargePrice
            else:
                return template.LargePrice

class Sub(models.Model):
    size = models.BooleanField(default = False)
    template = models.ForeignKey(TemplateSub , on_delete=models.CASCADE , related_name="dish")
    orders = models.ForeignKey(Order, on_delete=models.CASCADE , related_name="subs0_dish")
    Xcheese = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.template.name} - Small Size:{self.size} - ExtraCheese:{self.Xcheese} - Price:{self.price()}"

    def price(self):
        if self.size == False:
            if self.Xcheese == False:
                return self.template.SmallPrice
            else:
                return self.template.SmallPrice + self.template.XCheesePrice
        else:
            if self.Xcheese == False:
                return self.template.LargePrice
            else:
                return self.template.LargePrice + self.template.XCheesePrice

class DinnerPlatter(models.Model):
    size = models.BooleanField(default = False)
    template = models.ForeignKey(TemplateDinnerPlatter ,  on_delete=models.CASCADE ,related_name="dish")
    orders = models.ForeignKey(Order , on_delete=models.CASCADE , related_name="din_dish")

    def __str__(self):
        return f"{self.template.name} - Small Size:{self.size} - Price:{self.price()}"

    def price(self):
        if self.size == True:
            return self.template.LargePrice
        return self.template.SmallPrice

class Pasta(models.Model):
    orders = models.ForeignKey(Order , on_delete=models.CASCADE , related_name="pasta_dish")
    template = models.ForeignKey(TemplatePasta , on_delete=models.CASCADE , related_name="dish")

    def __str__(self):
        return f"{self.template.name} - Price:{self.price()}"

    def price(self):
        return self.template.SmallPrice

class Salad(models.Model):
    orders = models.ForeignKey(Order ,on_delete=models.CASCADE , related_name="salad_dish")
    template = models.ForeignKey(TemplateSalad , on_delete=models.CASCADE , related_name="dish")

    def __str__(self):
        return f"{self.template.name} - Price:{self.price()}"

    def price(self):
        return self.template.SmallPrice
