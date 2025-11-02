from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('recipes/', views.RecipeListView.as_view(), name='recipes-list'),
    path('recipes/add/', views.RecipeCreateView.as_view(), name='recipe-add'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
]
