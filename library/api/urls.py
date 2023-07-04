from django.urls import path
from . import views

urlpatterns = [
    path('v1/books/<str:pk>', views.BookAPI.as_view()),
    path('v1/books/', views.book_list, name="books"),
    path('v1/books_create/', views.BookCreate.as_view()),
    path('v1/authors/<str:pk>', views.AuthorApi.as_view()),
    path('v1/authors/', views.author_list, name="authors"),
    path('v1/authors_create/', views.AuthorCreate.as_view()),
    path('v1/orders/<str:pk>', views.OrderAPI.as_view()),
    path('v1/orders/', views.order_list, name="authors"),
    path('v1/orders_create/', views.OrderCreate.as_view())
]