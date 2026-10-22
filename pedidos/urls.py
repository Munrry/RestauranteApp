from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_menu, name='lista_menu'),
    path('cocina/', views.vista_cocina, name='vista_cocina'),
    path('mesa/<int:mesa_id>/cuenta/', views.detalle_cuenta, name='detalle_cuenta'),
    path('dashboard/', views.dashboard, name='dashboard'),
]