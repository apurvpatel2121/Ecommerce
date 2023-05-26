from django.contrib import admin
from store.models import Product,Variation,ReviewRating
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['product_name']}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value')
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)