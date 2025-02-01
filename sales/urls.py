from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pos/', views.pos, name='pos'),
    path('sales/', views.sale_list, name='sale_list'),
    path('sale/<int:pk>/', views.sale_detail, name='sale_detail'),
]