from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),
    path('change_language/', views.change_language_view, name="change_language"),
    path('search/', views.SearchView.as_view(), name="search"),
    path('search/clear/', views.SearchClearView.as_view(), name="search_clear"),
]
