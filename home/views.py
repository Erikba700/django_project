from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView

from helper.utils import advanced_search_products, get_search_data
from home.forms import RestaurantForm, restaurant_pizza_inline, restaurant_burger_inline
from home.models import Restaurant, FavoriteProduct
from pizza.models import Pizza, Burger


def about_us(request):
    return render(request, "home/about_us.html",
                  {"title": "About|Us"})


def restaurant_list(request):
    restaurants = Restaurant.objects.order_by("-pk")
    paginator = Paginator(restaurants, 4)
    page_number = request.GET.get('page')
    restaurants = paginator.get_page(page_number)
    return render(request, "home/restaurant_list.html",
                  context={"restaurants": restaurants, "title": "Restaurants"})


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.GET.get("burgers"):
        items = restaurant.burgers.all()
    else:
        items = restaurant.pizzas.all()
    return render(request, "home/restaurant_detail.html",
                  context={"restaurant": restaurant, "items": items})


def advanced_search(request):
    results = []
    if request.GET:
        if request.GET.get("type") == "burger":
            model = Burger
        else:
            model = Pizza
        search_data = get_search_data(request, model)
        results = advanced_search_products(model, search_data)

    return render(request, "home/advanced_search.html",
                  context={"results": results,
                           "restaurants": Restaurant.objects.all(),
                           "title": "ADVANCED|SEARCH"})


@login_required
def add_restaurant(request):
    related_data = []
    restaurant_form = RestaurantForm(request.POST or None, request.FILES or None)
    restaurant_pizza_formset = restaurant_pizza_inline(request.POST or None, request.FILES or None)
    restaurant_burger_formset = restaurant_burger_inline(request.POST or None, request.FILES or None)
    if restaurant_form.is_valid():
        for form in list(restaurant_pizza_formset) + list(restaurant_burger_formset):
            if form.is_valid():
                if form.cleaned_data:
                    instance = form.save(commit=False)
                    related_data.append(instance)
            else:
                for field, err in form.errors.items():
                    error_text = ','.join([e for e in err])
                    messages.error(request, f"{field}! {error_text}")
                    return redirect("home:add_restaurant")
        restaurant = restaurant_form.save(commit=False)
        restaurant.owner = request.user
        restaurant.save()
        restaurant.owner.profile.is_owner = True
        restaurant.owner.profile.save()
        for inst in related_data:
            inst.restaurant = restaurant
            inst.save()
        messages.success(request, f"Your {restaurant.name} Created Successfully")
        return redirect("home:restaurant_list")
    context = {"form": restaurant_form,
               "restaurant_burger_formset": restaurant_burger_formset,
               "restaurant_pizza_formset": restaurant_pizza_formset}
    return render(request, "home/add_restaurant.html", context)


class AddToCartView(TemplateView):
    product_map = {
        "pizza": Pizza,
        "burger": Burger
    }

    def get(self, request, model_class, product_id, *args, **kwargs):
        print(model_class)
        ProductModel = self.product_map.get(model_class)
        product = get_object_or_404(ProductModel, pk=product_id)
        product_content_type = ContentType.objects.get_for_model(product)
        if 'box' not in request.session:
            request.session['box'] = []
        request.session['box'].append({
            'content_type_id': product_content_type.id,
            'object_id': product.id,
        })
        request.session.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class RemoveFromCartView(TemplateView):
    product_map = {
        "pizza": Pizza,
        "burger": Burger
    }

    def get(self, request, model_class, product_id, *args, **kwargs):
        ProductModel = AddToCartView.product_map.get(model_class)
        product = get_object_or_404(ProductModel, pk=product_id)
        product_content_type = ContentType.objects.get_for_model(product)
        if 'box' in request.session:
            for item in request.session['box']:
                if item['content_type_id'] == product_content_type.id and item['object_id'] == product.id:
                    request.session['box'].remove(item)
                    request.session.save()
                    break
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CartListView(ListView):
    template_name = "home/cart_list.html"
    context_object_name = "cart_items"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Cart"
        return context

    def get_queryset(self):
        cart_items = []
        if 'box' in self.request.session:
            for item in self.request.session['box']:
                content_type = ContentType.objects.get(id=item['content_type_id'])
                model_class = content_type.model_class()
                product = model_class.objects.filter(id=item['object_id']).first()
                if product:
                    cart_items.append(product)
            return cart_items


class AddFavoriteView(LoginRequiredMixin, TemplateView):
    product_map = {
        "pizza": Pizza,
        "burger": Burger
    }

    def post(self, request, *args, **kwargs):
        content_type = request.POST.get("content_type")
        content_object = request.POST.get("content_object")
        model = self.product_map.get(content_type)
        if content_type and content_object:
            content_type = ContentType.objects.get_for_model(model=model)
            product = content_type.get_object_for_this_type(pk=int(content_object))
            request.user.favorite_products.create(content_object=product,
                                                  content_type=content_type)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class FavoriteProductsListView(LoginRequiredMixin, ListView):
    template_name = "home/favorite_list.html"
    model = FavoriteProduct

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Favorite"
        return context

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
