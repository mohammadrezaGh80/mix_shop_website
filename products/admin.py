from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, ProductColor, ProductSize, Product, ProductImage, Comment, Question, \
    CommentLike, CommentDislike, QuestionLike, QuestionDislike


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "parent")


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ("color_name",)


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ("size_name",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("image", "product",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "get_size", "get_color", "price", "created_datetime",)
    inlines = [
        ProductImageInline,
    ]

    def get_size(self, obj):
        return ", ".join([size.size_name for size in sizes]) if (sizes := obj.size.all()) else "-"

    get_size.short_description = _("Size")

    def get_color(self, obj):
        return ", ".join([color.color_name for color in colors]) if (colors := obj.color.all()) else "-"

    get_color.short_description = _("Color")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "product", "star_rating", "suggestion", "is_anonymous", "created_datetime")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("user", "get_text", "product", "created_datetime")

    def get_text(self, obj):
        return obj.text[:30]

    get_text.short_description = _("Text")


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "get_title_product", "modified_datetime")

    def get_title_product(self, obj):
        return obj.comment.product.title
    get_title_product.short_description = _("Title of product")


@admin.register(CommentDislike)
class CommentDislikeAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "get_title_product", "modified_datetime")

    def get_title_product(self, obj):
        return obj.comment.product.title
    get_title_product.short_description = _("Title of product")


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "get_title_product", "modified_datetime")

    def get_title_product(self, obj):
        return obj.comment.product.title
    get_title_product.short_description = _("Title of product")


@admin.register(QuestionDislike)
class QuestionDislikeAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "get_title_product", "modified_datetime")

    def get_title_product(self, obj):
        return obj.comment.product.title
    get_title_product.short_description = _("Title of product")

