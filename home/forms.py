from django import forms
from django.forms import inlineformset_factory

from home.models import Restaurant
from pizza.forms import PizzaForm, BurgerForm
from pizza.models import Pizza, Burger


class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ("name", "description", "address",
                  "phone", "website", "image")


restaurant_pizza_inline = inlineformset_factory(Restaurant, Pizza, extra=2,
                                                form=PizzaForm, can_delete=False)
restaurant_burger_inline = inlineformset_factory(Restaurant, Burger, extra=2,
                                                 form=BurgerForm, can_delete=False)

