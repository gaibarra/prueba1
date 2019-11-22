from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

from .models import Departamento, Funcionario
from .forms import DepartamentoForm, FuncionarioForm

from bases.views import SinPrivilegios



class VistaBaseCreate(SuccessMessageMixin,SinPrivilegios,generic.CreateView):
    context_object_name = 'obj'
    success_message="Registro Agregado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)



# Vista generica para actualizar registros


class VistaBaseEdit(SuccessMessageMixin,SinPrivilegios, generic.UpdateView):
    context_object_name = 'obj'
    success_message="Registro Actualizado Satisfactoriamente"

    def form_valid(self, form):
        #form.instance.um = self.request.user.id
        return super().form_valid(form)


class FuncionarioView(SinPrivilegios,generic.ListView):
        model = Funcionario
        template_name = "cat:funcionario_list.html"
        context_object_name = "obj"
        permission_required = "cat.view_funcionario"


class FuncionarioNew(VistaBaseCreate):
    model=Funcionario
    template_name="cat/funcionario_form.html"
    form_class=FuncionarioForm
    success_url= reverse_lazy("cat:funcionario_list")
    permission_required="cat.add_funcionario" 

class FuncionarioEdit(VistaBaseEdit):
    model=Funcionario
    template_name="cat/funcionario_form.html"
    form_class=FuncionarioForm
    success_url= reverse_lazy("cat:funcionario_list")
    permission_required="cat.change_funcionario"


@login_required(login_url="/login/")
@permission_required("cat.change_funcionario",login_url="/login/")
def funcionarioInactivar(request,id):
    funcionario = Funcionario.objects.filter(pk=id).first()

    if request.method=="POST":
        if funcionario:
            funcionario.estado = not funcionario.estado
            funcionario.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")          


class DepartamentoView(SinPrivilegios,generic.ListView):
        model = Departamento
        template_name = "cat:departamento_list.html"
        context_object_name = "obj"
        permission_required = "cat.view_departamento"


class DepartamentoNew(VistaBaseCreate):
    model=Departamento
    template_name="cat/departamento_form.html"
    form_class=DepartamentoForm
    success_url= reverse_lazy("cat:departamento_list")
    permission_required="cat.add_departamento" 

class DepartamentoEdit(VistaBaseEdit):
    model = Departamento
    template_name="cat/departamento_form.html"
    form_class = DepartamentoForm
    success_url= reverse_lazy("cat:departamento_list")
    permission_required="cat.change_departamento"


@login_required(login_url="/login/")
@permission_required("cat.change_departamento",login_url="/login/")
def departamentoInactivar(request,id):
    departamento = Departamento.objects.filter(pk=id).first()

    if request.method=="POST":
        if departamento:
            departamento.estado = not departamento.estado
            departamento.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")          

