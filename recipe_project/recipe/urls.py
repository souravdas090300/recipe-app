from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.RecipeListView.as_view(), name='recipes-list'),
    path('recipes/<pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
]
