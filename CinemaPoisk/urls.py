from django.contrib import admin
from django.urls import path
from CinemaPoisk import views
from loginsys import views as loginviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexRender),
    path('cinema/<int:cinemaid>', views.cinemaRender),
    path('movie/<int:movieid>', views.movieRender),
    path('person/<int:personid>', views.personRender),
    path('auth/login', loginviews.login),
    path('auth/logout', loginviews.logout),
    path('auth/register', loginviews.register)
]
