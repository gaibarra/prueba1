from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.


admin.site.register(SpyorEnc)
admin.site.register(SpyorDet)


class BeneficiarioResource(resources.ModelResource):
    class Meta:
        model = Beneficiario

class BeneficiarioAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['beneficiario']
    list_display = ('beneficiario', 'direccion', 'rfc', 'email', 'regimen')
    resource_class = BeneficiarioResource

admin.site.register(Beneficiario, BeneficiarioAdmin)