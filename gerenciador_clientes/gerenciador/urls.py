from django.contrib import admin
from django.urls import path, include
from clientes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/adicionar/', views.adicionar_cliente, name='adicionar_cliente'),
    path('clientes/editar/<int:cliente_id>/',
         views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:cliente_id>/',
         views.excluir_cliente, name='excluir_cliente'),


]
