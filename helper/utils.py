from django.db.models import Q


def similar_products(instance):
    model = instance.__class__
    q_instance = (
        Q(thick_type=instance.thick_type)
        if hasattr(instance, "thick_type")
        else Q(burger_type=instance.burger_type)
    )
    similar_data = model.objects.filter(
        (Q(price__gte=instance.price - 5) |
         Q(price__lte=instance.price + 5)) &
        q_instance
    ).exclude(id=instance.id)
    return similar_data


def advanced_search_products(model, search_data):
    result = model.objects.all()
    for search in search_data:
        result = result.filter(search)
    return result


def get_search_data(request, model):
    name = request.GET.get("pizza_name")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    thick_type = request.GET.get("thick_type")
    restaurant = request.GET.get("restaurant")
    search_data = []
    if name:
        search_data.append(Q(name__icontains=name))
    if min_price:
        if max_price:
            search_data.append(Q(price__gte=min_price) & Q(price__lte=max_price))
        else:
            search_data.append(Q(price__gte=min_price))
    elif max_price:
        search_data.append(Q(price__lte=max_price))
    if thick_type:
        if hasattr(model, "thick_type"):
            search_data.append(Q(thick_type=thick_type))
        elif hasattr(model, "burger_type"):
            search_data.append(Q(burger_type=thick_type))
    if restaurant:
        search_data.append(Q(restaurant=restaurant))
    return search_data
