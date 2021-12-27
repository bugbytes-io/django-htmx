from django.urls import path
from films import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("films/", views.FilmList.as_view(), name='film-list'),
]

htmx_urlpatterns = [
    path('check_username/', views.check_username, name='check-username'),
    path('add-film/', views.add_film, name='add-film'),
    path('delete-film/<int:pk>/', views.delete_film, name='delete-film'),
    path('search-film/', views.search_film, name='search-film'),
    path('clear/', views.clear, name='clear'),
    path('sort/', views.sort, name='sort'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('film-list-partial', views.films_partial, name='film-list-partial'),
    path('upload-photo/<int:pk>/', views.upload_photo, name='upload-photo'),
    
]

urlpatterns += htmx_urlpatterns