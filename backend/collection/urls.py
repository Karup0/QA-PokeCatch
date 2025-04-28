from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('capture/', views.capture_pokemon, name='capture'),
    path('captured/', views.captured_pokemon, name='captured'),
    path('missing/', views.missing_pokemon, name='missing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:pokemon_id>/', views.delete_pokemon, name='delete_pokemon'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
