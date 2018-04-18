from django.urls import path
from . import views


urlpatterns = [
    path('', views.SearchMainView.as_view(), name="search_main_view"),
    path('results/', views.SearchResultsView.as_view(), name="search_results"),
]
