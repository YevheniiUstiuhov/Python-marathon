from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login_user", views.login_user, name="login"),
    path("register_user", views.register_user, name="register"),
    path("logout_user", views.logout_user, name="logout"),
    path('users', views.get_users, name='users_list'),
    path('users/<int:user_id>', views.user_detail, name='user_detail'),

]
