"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Добавляем маршрут для главной страницы
    path('about', views.aboutpage, name='about'),  # Добавляем маршрут для главной страницы
    path('login', views.user_login, name='loginpage'),
    path('signup', views.signup, name='signuppage'),
    path('signupdone', views.signupdone, name='signupdone'),
    path('posts', views.posts, name='posts'),
    path('logout', views.logout_view, name='logout'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/add/', views.add_post, name='add_post'),
]
