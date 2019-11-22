from django.urls import path, include
from .views import *


urlpatterns = [
    path('spyors/',SpyorView.as_view(), name="spyorenc_list"),
    path('spyors/new',spyors, name="spyors_new"),
    path('spyors/edit/<int:solicitud_id>',spyors, name="spyors_edit"),
    path('spyors/buscar-funcionario',FuncionarioView.as_view(), name="buscar_funcionario"),
    path('spyors/<int:solicitud_id>/delete/<int:pk>',SpyorDetDelete.as_view(), name="spyor_del"),


    path('beneficiarios/',BeneficiarioView.as_view(), name="beneficiario_list"),
    path('beneficiarios/new',BeneficiarioNew.as_view(), name="beneficiario_new"),
    path('beneficiarios/<int:pk>',BeneficiarioEdit.as_view(), name="beneficiario_edit"),
    path('beneficiarios/estado/<int:id>',beneficiarioInactivar, name="beneficiario_inactivar"),

    path('upload',upload, name="upload"),
]
