from django.urls import path, include

from .views import  *

urlpatterns = [
    path('departamentos/',DepartamentoView.as_view(), name="departamento_list"),
    path('departamentos/new',DepartamentoNew.as_view(), name="departamento_new"),
    path('departamentos/<int:pk>',DepartamentoEdit.as_view(), name="departamento_edit"),
    path('departamentos/estado/<int:id>',departamentoInactivar, name="departamento_inactivar"),
    
    path('funcionarios/',FuncionarioView.as_view(), name="funcionario_list"),
    path('funcionarios/new',FuncionarioNew.as_view(), name="funcionario_new"),
    path('funcionarios/<int:pk>',FuncionarioEdit.as_view(), name="funcionario_edit"),
    path('funcionarios/estado/<int:id>',funcionarioInactivar, name="funcionario_inactivar"),
]