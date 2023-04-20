from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.ProfilePageTemplateView.as_view(), name="profile_page"),
    path("orders/", views.OrdersTemplateView.as_view(), name="orders"),
    path("favorites/", views.FavoritesTemplateView.as_view(), name="favorites_list"),
    path("comments/", views.CommentsTemplateView.as_view(), name="comments"),
    path("addresses/", views.AddressesTemplateView.as_view(), name="addresses"),
    path("messages/", views.MessagesTemplateView.as_view(), name="messages"),
    path("recent_visits/", views.RecentVisitsTemplateView.as_view(), name="recent_visits"),
    path("personal_info/", views.PersonalInfoUpdateView.as_view(), name="personal_info"),
]
