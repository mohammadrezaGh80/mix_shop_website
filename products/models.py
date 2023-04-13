from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core import validators


class Category(models.Model):
    DIGITAL_PRODUCT = _("digital product")
    CLOTHING = _("clothing")
    STATIONERY = _("stationery")
    BEAUTY_AND_HEALTH = _("beauty and health")

    category_name = models.CharField(max_length=100, verbose_name=_("Category's name"))

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class SubCategory(models.Model):
    PHONE = _("phone")
    TELEVISION = _("television")
    LAPTOP = _("laptop")
    CAMERA = _("camera")
    GAME_CONSOLE = _("game console")
    MENSWEAR = _("menswear")
    WOMEN_DRESS = _("women's dress")
    MEN_SHOES = _("men's shoes")
    WOMEN_SHOES = _("women's shoes")
    NOTEBOOK = _("notebook")
    PENCIL = _("pencil")
    DESK = _("desk")
    COSMETIC = _("cosmetic")
    SANITARY_WARE = _("sanitary ware")

    sub_category_name = models.CharField(max_length=150, verbose_name=_("Sub category's name"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="sub_categories", verbose_name=_("Category"))

    def __str__(self):
        return f"{self.sub_category_name}({self.category.category_name})"

    class Meta:
        verbose_name = _("Sub category")
        verbose_name_plural = _("Sub categories")


class ProductColor(models.Model):
    RED = _("red")
    BLUE = _("blue")
    BLACK = _("black")
    WHITE = _("white")
    PINK = _("pink")
    YELLOW = _("yellow")
    BROWN = _("brown")
    PURPLE = _("purple")
    GREEN = _("green")
    ORANGE = _("orange")
    GRAY = _("gray")
    GOLDEN = _("golden")
    SILVER = _("silver")
    BRONZE = _("bronze")

    color_name = models.CharField(max_length=100, verbose_name=_("Color's name"))

    def __str__(self):
        return self.color_name

    class Meta:
        verbose_name = _("Product color")
        verbose_name_plural = _("Product colors")


class ProductSize(models.Model):
    SM = "sm"
    M = "m"
    L = "l"
    XL = "xl"
    XXL = "xxl"
    XXXL = "3xl"
    XXXXL = "4xl"

    size_name = models.CharField(max_length=50, verbose_name=_("Size's name"))

    def __str__(self):
        return self.size_name

    class Meta:
        verbose_name = _("Product size")
        verbose_name_plural = _("Product sizes")


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name=_("Title"))
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               related_name="products", verbose_name=_("Seller"))
    price = models.DecimalField(
        max_digits=11,
        decimal_places=0,
        validators=[validators.MinValueValidator(1, message=_("The value of the price cannot be negative or zero."))],
        verbose_name=_("Price")
    )
    color = models.ManyToManyField(ProductColor, related_name="products", blank=True, verbose_name=_("Color"))
    size = models.ManyToManyField(ProductSize, related_name="products", blank=True, verbose_name=_("Size"))
    description = models.TextField(verbose_name=_("Description"))

    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_("Created datetime"))
    modified_datetime = models.DateTimeField(auto_now=True, verbose_name=_("Modified datetime"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductImage(models.Model):
    image = models.ImageField(upload_to="product/product_image/", verbose_name=_("Image"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name=_("Product"))

    def __str__(self):
        return f"Image for {self.product.title}"

    class Meta:
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")
