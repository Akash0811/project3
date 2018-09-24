from django.db import models
from django.utils.timezone import now

# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=64 , default = "MyOrder")
    time = now()
    pass

class NonSizableDish(models.Model):
    name = models.CharField(max_length=64)
    orders = models.ManyToManyField(Order, blank=True, related_name="dish")
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

class RegularPizza(SizableDish):
    toppings = models.ManyToManyField(Topping, blank=True, related_name="reg_dish")

class SicilianPizza(SizableDish):
    toppings = models.ManyToManyField(Topping, blank=True, related_name="sic_dish")

class Sub(SizableDish):
    Xcheese = models.ManyToManyField(ExtraCheese , related_name = "subs_dish")
    XCheesePrice = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name} - Small:{self.SmallPrice} - Large:{self.LargePrice} - ExtraCheese:{self.XCheesePrice}"

class DinnerPlatter(SizableDish):
    pass

class Pasta(NonSizableDish):
    pass

class Salad(NonSizableDish):
    pass
