from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.conf import settings


class Restaurant(models.Model):
    """A model for a restaurant."""
    name = models.CharField(max_length=50)
    description = models.TextField()
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15)
    website = models.URLField(blank=True)
    image = models.ImageField(upload_to="restaurant_images")
    owner = models.ForeignKey("users.Profile", on_delete=models.CASCADE,
                              related_name="restaurants")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("home:restaurant_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Tag(models.Model):
    """A model for a tag."""
    name = models.CharField(max_length=50)
    pizza = models.ManyToManyField("pizza.Pizza", related_name="tags")
    burger = models.ManyToManyField("pizza.Burger", related_name="tags")

    def __str__(self):
        return self.name


class AbstractProduct(models.Model):
    """An abstract model for a product."""

    @property
    def get_model_name(self):
        return self.__class__.__name__.lower()

    class Meta:
        abstract = True


class FavoriteProduct(models.Model):
    """A model for a favorite product not a card be careful."""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='favorite_products')

