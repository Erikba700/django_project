from django.db import models


class PizzaThickChoice(models.TextChoices):
    THIN = "thin", "Thin"
    THICK = "thick", "Thick"


class BurgerSizeChoice(models.TextChoices):
    SMALL = "small", "Small"
    MEDIUM = "medium", "Medium"
    LARGE = "large", "Large"
