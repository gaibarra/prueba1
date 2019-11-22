from django.shortcuts import render,redirect
from django.views import generic

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

from django.contrib.auth import authenticate
from bases.views import SinPrivilegios
from cat.models import Departamento, Funcionario
from dto.models import SpyorEnc, SpyorDet, Beneficiario
from cat.forms import DepartamentoForm, FuncionarioForm
from .forms import BeneficiarioForm, SpyorEncForm
from django.core.files.storage import FileSystemStorage


import cat.views as cat
from cat.models import Funcionario

class FuncionarioView(cat.FuncionarioView):
   template_name= "dto/buscar_funcionario.html"


class BeneficiarioView(SinPrivilegios,generic.ListView):
    model = Beneficiario
    template_name = "dto:beneficiario_list.html"
    context_object_name = "obj"
    permission_required = "dto.view_beneficiario"


class BeneficiarioNew(cat.VistaBaseCreate):
    model = Beneficiario
    template_name="dto/beneficiario_form.html"
    form_class = BeneficiarioForm
    success_url= reverse_lazy("dto:beneficiario_list")
    permission_required="dto.add_beneficiario" 

class BeneficiarioEdit(cat.VistaBaseEdit):
    model = Beneficiario
    template_name="dto/beneficiario_form.html"
    form_class = BeneficiarioForm
    success_url= reverse_lazy("dto:beneficiario_list")
    permission_required="dto.change_beneficiario"


@login_required(login_url="/login/")
@permission_required("dto.change_beneficiario",login_url="/login/")
def beneficiarioInactivar(request,id):
    beneficiario = Beneficiario.objects.filter(pk=id).first()

    if request.method=="POST":
        if beneficiario:
            beneficiario.estado = not beneficiario.estado
            beneficiario.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")          






class SpyorView(SinPrivilegios, generic.ListView):
    model = SpyorEnc
    template_name = "dto/spyor_list.html"
    context_object_name = "obj"
    permission_required="dto.view_spyorenc"

    def get_queryset(self):
          return SpyorEnc.objects.filter(uc_id=self.request.user)



@login_required(login_url='/login/')
@permission_required('dto.change_spyorenc', login_url='bases:sin_privilegios')
def spyors(request,solicitud_id=None):
    template_name='dto/spyors.html'
    
    detalle = {}
    beneficiarios =Beneficiario.objects.filter(estado=True)
    funcionarios = Funcionario.objects.filter(estado=True)
    departamentos =Departamento.objects.filter(estado=True)
    
    if request.method == "GET":
        enc = SpyorEnc.objects.filter(pk=solicitud_id).first()
        if not enc:
            encabezado = {
                'id':"",
                'fecha_solicitud':datetime.today(),
                'beneficiario':" ",
                'funcionario':" ",
                'comentarios':"",
                'imp_total':0.00,
                'numero_cheque':" ",
                'fecha_cheque':" ", 
                
                'status':" ",
            }
            detalle=None
        else:
            encabezado = {
                'id':enc.id,
                'fecha_solicitud':enc.fecha_solicitud,
                'beneficiario':enc.beneficiario,
                'funcionario':enc.funcionario,
                'comentarios':enc.comentarios,
                'imp_total':enc.imp_total,
                'numero_cheque':enc.numero_cheque,
                'fecha_cheque':enc.fecha_cheque,
                'status':enc.status
            }

        detalle=SpyorDet.objects.filter(solicitud=enc)
       
        contexto = {"enc":encabezado,"det":detalle,"beneficiarios":beneficiarios,"departamentos":departamentos,"funcionarios":funcionarios,}
        return render(request,template_name,contexto)
    
    if request.method == "POST":
        beneficiario = request.POST.get("enc_beneficiario")
        funcionario = request.POST.get("enc_funcionario")
        comentarios = request.POST.get("comentarios")
        fecha_solicitud  = request.POST.get("fecha_solicitud")
        status = request.POST.get("status")
        cli=Beneficiario.objects.get(pk=beneficiario)
        fun=Funcionario.objects.get(pk=funcionario)

        if not solicitud_id:
            enc = SpyorEnc(
                beneficiario = cli,
                funcionario = fun,
                comentarios = comentarios,
                fecha_solicitud = fecha_solicitud,
                status = status
            )
            if enc:
                enc.save()
                solicitud_id = enc.id
        else:
            enc = SpyorEnc.objects.filter(pk=solicitud_id).first()
            if enc:
                enc.beneficiario = cli
                enc.funcionario = fun
                enc.comentarios = comentarios
                enc.save()

        if not id:
            messages.error(request,'No Puedo Continuar No Pude Detectar No. de Solicitud')
            return redirect("dto:spyorenc_list")
        
        

        tipo_comprobante = request.POST.get("tipo_comprobante")
        no_facturasol = request.POST.get("no_facturasol")
        fecha_compra = request.POST.get("fecha_compra")
        importe = request.POST.get("importe")
        descripcion = request.POST.get("descripcion")
        departamento = request.POST.get("departamento")
        dep=Departamento.objects.get(pk=departamento)
        imagen1= request.POST.get('imagen1')





        #func = Funcionario.objects.get(codigo=Funcionario.codigo)
        
        det = SpyorDet(
            solicitud=enc,
            tipo_comprobante=tipo_comprobante,
            no_facturasol=no_facturasol,
            fecha_compra=fecha_compra,
            importe=importe,
            departamento=dep,
            descripcion=descripcion,
            imagen1=imagen1,
            
        )
        
        if det:
            det.save()
            
        
            return redirect("dto:spyors_edit",solicitud_id=solicitud_id)

    return render(request,template_name,contexto)


class SpyorDetDelete(SinPrivilegios, generic.DeleteView):
    permission_required = "dto.delete_spyordet"
    model = SpyorDet
    template_name = "dto/spyor_det_del.html"
    context_object_name = 'obj'
    
    def get_success_url(self):
          
          solicitud_id=self.kwargs['solicitud_id']
          return reverse_lazy('dto:spyors_edit', kwargs={'solicitud_id': solicitud_id})


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url']= fs.url(name)
    return render(request, 'dto/upload.html')