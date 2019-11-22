from django.urls import path, include
from .views import *

urlpatterns = [
    path('v1/funcionarios/',FuncionarioList.as_view(),name='funcionario_list'),
    path('v1/funcionarios/<str:codigo>',FuncionarioDetalle.as_view(),name='funcionario_detalle'),
]