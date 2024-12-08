from django import forms

from pizza.models import Pizza, Burger


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ("name", "description", "price", "rate",
                  "thick_type", "image", "restaurant")


class BurgerForm(forms.ModelForm):

    class Meta:
        model = Burger
        fields = ("name", "description", "price", "rate",
                  "burger_type", "image", "restaurant")
