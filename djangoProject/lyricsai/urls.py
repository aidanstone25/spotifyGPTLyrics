from . import views
from django.urls import path
urlpatterns = [
    path('',views.home, name='home'),
    path('search',views.search,name='search'),
    path('search_results',views.search_results,name='search_results'),]