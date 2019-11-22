from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import DepartamentoSerializer, FuncionarioSerializer
from cat.models import Departamento, Funcionario

from django.db.models import Q

class DepartamentoList(APIView):
    def get(self,request):
        depa = Departamento.objects.all()
        data = DepartamentoSerializer(depa,many=True).data
        return Response(data)


class DepartamentoDetalle(APIView):
    def get(self,request, clavedepto):
        depa = get_object_or_404(Departamento,Q(clavedepto=clavedepto))
        data = DepartamentoSerializer(depa).data
        return Response(data)


class FuncionarioList(APIView):
    def get(self,request):
        func = Funcionario.objects.all()
        data = FuncionarioSerializer(func,many=True).data
        return Response(data)


class FuncionarioDetalle(APIView):
    def get(self,request, codigo):
        func = get_object_or_404(Funcionario,Q(codigo=codigo))
        data = FuncionarioSerializer(func).data
        return Response(data)
