from django.urls import path
from . import views

app_name = "outgoing"

urlpatterns = [
    path('', views.outgoing, name='outgoing'),
    path('new/', views.new, name='new'),
    path('list/', views.outgoing, name='list'),
    path('graph/', views.graph, name='graph'),
    path('edit/<int:id>/', views.edit_article, name='edit_article'),  
    path('delete/<int:id>/', views.delete_article, name='delete_article'),
    path('update-models/', views.update_models, name='update_models'),
]
