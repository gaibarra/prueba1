from django import forms

from .models import Departamento, Funcionario




class DepartamentoForm(forms.ModelForm):
    class Meta:
        model=Departamento
        fields=['clavedepto','departamento','estado']
        exclude = ['um','fm','uc','fc']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model=Funcionario
        fields=['codigo','nombre_funcionario','clave_depto','rfc','curp',
             'fecha_ingreso','email', 'grupo','imss','estado']
        exclude = ['um','fm','uc','fc']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

