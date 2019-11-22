from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class FuncionarioResource(resources.ModelResource):
    class Meta:
        model = Funcionario

class FuncionarioAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['nombre_funcionario']
    list_display = ('codigo', 'nombre_funcionario','clave_depto', 'rfc', 'curp','imss')
    resource_class = FuncionarioResource

admin.site.register(Funcionario, FuncionarioAdmin)

class DepartamentoResource(resources.ModelResource):
    class Meta:
        model = Departamento

class DepartamentoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['departamento']
    list_display = ('clavedepto', 'departamento')
    resource_class = DepartamentoResource

admin.site.register(Departamento, DepartamentoAdmin)