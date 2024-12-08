from django.urls import path
from home import views

app_name = "home"
urlpatterns = [
    path("about-us/", views.about_us, name="about_us"),
    path("restaurant-list/", views.restaurant_list, name="restaurant_list"),
    path("restaurant-detail/<int:pk>/", views.restaurant_detail, name="res_detail"),
    path("advanced-search/", views.advanced_search, name="advanced_search"),
    path("add-restaurant/", views.add_restaurant, name="add_restaurant"),
    path("add-to-cart/<str:model_class>/<int:product_id>",
         views.AddToCartView.as_view(), name="add_to_cart"),
    path("remove-from-cart/<str:model_class>/<int:product_id>",
         views.RemoveFromCartView.as_view(), name="remove_from_cart"),
    path("cart/", views.CartListView.as_view(), name="cart"),
    path("add-favorite/", views.AddFavoriteView.as_view(), name="add_favorite"),
    path("wish-list/", views.FavoriteProductsListView.as_view(), name="favorite_products"),
]
