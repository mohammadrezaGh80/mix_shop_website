from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core import validators

from ckeditor.fields import RichTextField


class Category(models.Model):
    DIGITAL_PRODUCT = _("digital-product")
    CLOTHING = _("clothing")
    STATIONERY = _("stationery")
    BEAUTY_AND_HEALTH = _("beauty-and-health")
    SMART_PHONE = _("smart-phone")

    TELEVISION = _("television")
    LAPTOP = _("laptop")
    CAMERA = _("camera")
    GAME_CONSOLE = _("game-console")
    MENSWEAR = _("menswear")
    WOMEN_DRESS = _("women's-dress")
    MEN_SHOES = _("men's-shoes")
    WOMEN_SHOES = _("women's-shoes")
    NOTEBOOK = _("notebook")
    PENCIL = _("pencil")
    DESK = _("desk")
    COSMETIC = _("cosmetic")
    SANITARY_WARE = _("sanitary-ware")
    XIAOMI = _("xiaomi")
    APPLE = _("apple")
    SAMSUNG = _("samsung")

    category_name = models.CharField(max_length=150, verbose_name=_("Category's name"))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name="sub_categories", verbose_name=_("Category"))

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


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
    description = RichTextField(verbose_name=_("Description"))
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, verbose_name=_("Category"))

    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_("Created datetime"))
    modified_datetime = models.DateTimeField(auto_now=True, verbose_name=_("Modified datetime"))

    def get_absolute_url(self):
        return reverse("products:product_detail", args=[self.category.category_name, self.pk])

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


class Comment(models.Model):
    ONE_STAR = 1
    TWO_STAR = 2
    THREE_STAR = 3
    FOUR_STAR = 4
    FIVE_STAR = 5

    NONE = 0
    I_SUGGEST = 1
    I_DONT_SUGGEST = 2
    I_AM_NOT_SURE = 3

    STAR_CHOICES = (
        (ONE_STAR, _("1 star")),
        (TWO_STAR, _("2 star")),
        (THREE_STAR, _("3 star")),
        (FOUR_STAR, _("4 star")),
        (FIVE_STAR, _("5 star")),
    )
    suggestion_CHOICES = (
        (NONE, _("None")),
        (I_SUGGEST, _("I suggest")),
        (I_DONT_SUGGEST, _("I don't suggest")),
        (I_AM_NOT_SURE, _("I'm not sure")),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments", verbose_name=_("User"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments", verbose_name=_("Product"))
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Title"))
    text = models.TextField(verbose_name=_("Text"))
    star_rating = models.PositiveSmallIntegerField(choices=STAR_CHOICES, verbose_name=_("Star rating"))
    suggestion = models.PositiveSmallIntegerField(default=NONE, choices=suggestion_CHOICES, blank=True,
                                                  verbose_name=_("Suggestion"))
    is_anonymous = models.BooleanField(default=False, verbose_name=_("Is anonymous?"))
    number_of_likes = models.PositiveIntegerField(default=0, verbose_name=_("Number of likes"))
    number_of_dislikes = models.PositiveIntegerField(default=0, verbose_name=_("Number of dislikes"))

    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_("Created datetime"))
    modified_datetime = models.DateTimeField(auto_now=True, verbose_name=_("Modified datetime"))

    def __str__(self):
        return f"{self.title}({self.user.email}) --> {self.product.title}"

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


class Question(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="questions", verbose_name=_("User"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="questions", verbose_name=_("Product"))
    text = models.CharField(max_length=100, verbose_name=_("Text"))
    number_of_likes = models.PositiveIntegerField(default=0, verbose_name=_("Number of likes"))
    number_of_dislikes = models.PositiveIntegerField(default=0, verbose_name=_("Number of dislikes"))

    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_("Created datetime"))
    modified_datetime = models.DateTimeField(auto_now=True, verbose_name=_("Modified datetime"))

    def __str__(self):
        return f"{self.text[:30]}({self.user.email}) --> {self.product.title}"

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
