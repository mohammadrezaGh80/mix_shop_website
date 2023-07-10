from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path('<str:category_name>/', views.ProductCategoryView.as_view(), name="product_category"),
    path('search/<str:category_name>/', views.ProductSubCategoryListView.as_view(), name="product_sub_category_list"),
    path('search/<str:category_name>/<int:pk>/', views.ProductDetailView.as_view(), name="product_detail"),
    path('search/<str:category_name>/<int:id_product>/like/<int:id_comment>/comment/', views.ProductLikeComment.as_view(),
         name="product_like_comment"),
    path('search/<str:category_name>/<int:id_product>/dislike/<int:id_comment>/comment/', views.ProductDislikeComment.as_view(),
         name="product_dislike_comment"),
    path('search/<str:category_name>/<int:id_product>/like/<int:id_answer>/answer/', views.ProductLikeAnswer.as_view(),
         name="product_like_answer"),
    path('search/<str:category_name>/<int:id_product>/dislike/<int:id_answer>/answer/', views.ProductDislikeAnswer.as_view(),
         name="product_dislike_answer"),
]
