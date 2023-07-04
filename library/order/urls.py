from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('all_orders', views.all_orders, name='all_orders'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('create_order/', views.create_order, name='create_order'),
    path('close_order/<int:pk>/', views.close_order, name='close_order'),
]
