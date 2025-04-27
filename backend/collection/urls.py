from django.urls import path
from . import views

urlpatterns = [ 
    path('capture/', views.capture_pokemon, name='capture'),
    path('captured/', views.captured_pokemon, name='captured'),
    path('missing/', views.missing_pokemon, name='missing'),  # 🆕
    path('trade/', views.trade_pokemon, name='trade'),        # 🆕
]
