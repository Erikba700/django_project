from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from helper.utils import similar_products
from helper.validators import is_owner_validator
from pizza.forms import PizzaForm, BurgerForm
from pizza.models import Pizza, Burger


# Create your views here.

def list_pizza(request):
    pizza_list = Pizza.objects.all()
    paginator = Paginator(pizza_list, 3)
    page_number = request.GET.get('page')
    pizza_list = paginator.get_page(page_number)
    return render(request, "pizza/list_pizza.html",
                  {"pizzas": pizza_list, "title": "Pizzas"})


def pizza_detail(request, pk):
    pizza = get_object_or_404(Pizza, pk=pk)
    similar_pizzas = similar_products(pizza)
    return render(request, "pizza/pizza_detail.html",
                  {"pizza": pizza,
                   "similar_pizzas": similar_pizzas,
                   "title": "pizza"})


def burger_list(request):
    burgers = Burger.objects.all()
    paginator = Paginator(burgers, 3)
    page_number = request.GET.get('page')
    burgers = paginator.get_page(page_number)
    return render(request, "burger/burger_list.html",
                  {"burgers": burgers, "title": "Burgers"})


def burger_detail(request, pk):
    burger = get_object_or_404(Burger, pk=pk)
    similar_burgers = similar_products(burger)
    return render(request, "burger/burger_detail.html",
                  {"burger": burger,
                   "similar_burgers": similar_burgers,
                   "title": "burger"})


@is_owner_validator(model=Pizza)
@login_required
def add_pizza(request):
    form = PizzaForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save()
            messages.success(request, "Pizza added successfully")
            return redirect("pizza:list")
    return render(request, "pizza/add_pizza.html",
                  {"form": form})


@is_owner_validator(model=Burger)
@login_required
def add_burger(request):

    form = BurgerForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save()
            messages.success(request, "Burger added successfully")
            return redirect("pizza:burger_list")
    return render(request, "burger/add_burger.html",
                  {"form": form})


def tag_pizza_view(request, tag):
    pizzas = Pizza.objects.filter(tags__name__iexact=tag)
    return render(request, "pizza/tag_pizza.html",
                  {"pizzas": pizzas, "title": tag})


def tag_burger_view(request, tag):
    burgers = Burger.objects.filter(tags__name__iexact=tag)
    return render(request, "burger/tag_burger.html",
                  {"burgers": burgers, "title": tag})
