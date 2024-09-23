from django.urls import path
from . import views

app_name = 'inventory'


urlpatterns = [
    path('types/', views.type_list, name='type_list'),  # List of types
    path('types/add/', views.add_type, name='add_type'),  # Add a new type
    path('types/edit/<int:pk>/', views.edit_type, name='edit_type'),  # Edit a type
    path('types/delete/<int:pk>/', views.delete_type, name='delete_type'),  # Delete a type
    path('models/', views.model_list, name='model_list'),  # List of models
    path('models/add/', views.add_model, name='add_model'),  # Add a new model
    path('models/edit/<int:pk>/', views.edit_model, name='edit_model'),  # Edit model URL
    path('models/delete/<int:pk>/', views.delete_model, name='delete_model'),  # Delete model URL
]
