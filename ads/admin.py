from django.contrib import admin
from .models import Category, Ad

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'is_active', 'views_count')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'text')