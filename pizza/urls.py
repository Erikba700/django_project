from django.urls import path
from pizza import views

app_name = "pizza"
urlpatterns = [
    path("", views.list_pizza, name="list"),
    path("pizza/<int:pk>/", views.pizza_detail, name="detail"),
    path("add-pizza/", views.add_pizza, name="add_pizza"),
    path("burger/list/", views.burger_list, name="burger_list"),
    path("burger/<int:pk>/", views.burger_detail, name="burger_detail"),
    path("add-burger/", views.add_burger, name="add_burger"),
    path("tag/pizza/<str:tag>/", views.tag_pizza_view, name="tag_pizza"),
    path("tag/burger/<str:tag>/", views.tag_burger_view, name="tag_burger")
]
