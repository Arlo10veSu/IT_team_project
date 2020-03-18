from django.contrib import admin
from rango.models import *


class DishAdmin(admin.ModelAdmin):
    list_display = ('category', 'dish', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category',)}


class RemarkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'mail', 'topic', 'message')


admin.site.register(Remark, RemarkAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(UserProfile)
admin.site.register(UserInfor)
admin.site.register(UserComment)
