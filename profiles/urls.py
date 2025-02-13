from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.ProfilePageTemplateView.as_view(), name="profile_page"),
    path("orders/", views.OrdersTemplateView.as_view(), name="orders"),
    path("favorites/", views.FavoritesTemplateView.as_view(), name="favorites_list"),
    path("comments/", views.ManageCommentView.as_view(), name="comments"),
    path("comments/<int:pk>/delete/", views.DeleteCommentView.as_view(), name="comment_delete"),
    path("addresses/", views.AddressesTemplateView.as_view(), name="addresses"),
    path("recent_visits/", views.RecentVisitsTemplateView.as_view(), name="recent_visits"),
    path("recent_visits/clear/", views.ClearRecentVisits.as_view(), name="clear_recent_visits"),
    path("personal_info/", views.PersonalInfoUpdateView.as_view(), name="personal_info"),
    path("recent_visits/delete/", views.DeleteProductOfRecentVisits.as_view(), name="delete_product_recent_visits"),
]
