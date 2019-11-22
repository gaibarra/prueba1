from django import forms

from .models import Departamento, Beneficiario, SpyorEnc, SpyorDet


class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model= Beneficiario
        fields=['beneficiario','direccion','rfc','email','regimen','estado']
        exclude = ['um','fm','uc','fc']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class SpyorEncForm(forms.ModelForm):
    fecha_solicitud = forms.DateInput()
    fecha_cheque = forms.DateInput()
    
    class Meta:
        model=SpyorEnc
        fields=['fecha_solicitud','beneficiario','imp_total',
            'numero_cheque','fecha_cheque','comentarios']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        
        self.fields['fecha_solicitud'].widget.attrs['readonly'] = True
        
