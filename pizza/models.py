from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from helper.choices import PizzaThickChoice, BurgerSizeChoice
from helper.upload import upload_pizza_image
from home.models import AbstractProduct


class Pizza(AbstractProduct, models.Model):

    name = models.CharField(max_length=100,)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to=upload_pizza_image)
    thick_type = models.CharField(max_length=100, choices=PizzaThickChoice.choices,
                                  default=PizzaThickChoice.THIN)
    rate = models.DecimalField(max_digits=3, decimal_places=2,
                               validators=[MinValueValidator(0), MaxValueValidator(5)],
                               default=0.0)
    restaurant = models.ForeignKey("home.Restaurant",
                                   on_delete=models.CASCADE,
                                   related_name="pizzas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("pizza:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Burger(AbstractProduct, models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    rate = models.DecimalField(max_digits=3, decimal_places=2,
                               validators=[MinValueValidator(0), MaxValueValidator(5)],
                               default=0.0)
    burger_type = models.CharField(max_length=10, choices=BurgerSizeChoice.choices)
    image = models.ImageField(upload_to="burger_images")
    restaurant = models.ForeignKey("home.Restaurant",
                                   on_delete=models.CASCADE,
                                   related_name="burgers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("pizza:burger_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name
