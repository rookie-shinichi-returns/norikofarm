from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('', views.plant_imagelist.as_view(), name='plant_imagelist'),
    path('add/', views.image_add.as_view(), name='image_add'),
    path('update/<int:pk>/', views.image_update.as_view(), name='image_update'),
    path('index/', views.index.as_view(), name='index'),
]