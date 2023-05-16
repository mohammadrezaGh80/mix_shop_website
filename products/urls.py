from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path('<str:category_name>/', views.ProductCategoryView.as_view(), name="product_category"),
    path('search/<str:category_name>/', views.ProductSubCategoryListView.as_view(), name="product_sub_category_list"),
    path('search/<str:category_name>/<int:pk>/', views.ProductDetailView.as_view(), name="product_detail"),
]
