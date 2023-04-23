from category.models import Category

def menu_list(request):
    categories = Category.objects.all().order_by("category_name")
    return dict(categories=categories)