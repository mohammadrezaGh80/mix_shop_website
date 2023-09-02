from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.CartDetailView.as_view(), name="cart_detail"),
    path("add/<int:pk>/", views.AddToCartProductView.as_view(), name="cart_add_product"),
    path("remove/<int:pk>/", views.RemoveFromCartProductView.as_view(), name="cart_remove_product"),
    path("clear/", views.ClearCartView.as_view(), name="cart_clear"),
]
