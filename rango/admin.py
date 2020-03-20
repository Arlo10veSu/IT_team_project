from django.contrib import admin

from rango.forms import CommentForm
from rango.models import *


class DishAdmin(admin.ModelAdmin):
    list_display = ('category', 'dish', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(UserProfile)
admin.site.register(UserComment)
