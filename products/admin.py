from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, ProductColor, ProductSize, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "parent")


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ("color_name", )


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ("size_name", )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("image", "product", )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "get_size", "get_color", "price", "created_datetime", )
    inlines = [
        ProductImageInline,
    ]

    def get_size(self, obj):
        return ", ".join([size.size_name for size in sizes]) if (sizes := obj.size.all()) else "-"
    get_size.short_description = _("Size")

    def get_color(self, obj):
        return ", ".join([color.color_name for color in colors]) if (colors := obj.color.all()) else "-"
    get_color.short_description = _("Color")
