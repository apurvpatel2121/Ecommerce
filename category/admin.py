from django.contrib import admin
from category.models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['category_name']}
    ordering = ('category_name',)

admin.site.register(Category,CategoryAdmin)
