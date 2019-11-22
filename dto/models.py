from django.db import models

#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from bases.models import ClaseModelo, ClaseModelo2
from cat.models import Departamento, Funcionario
from ckeditor.fields import RichTextField
from djmoney.models.fields import MoneyField
from django.utils import timezone


# Create your models here.
COMPROBANTE_CHOICES= [
    ('fac', 'Factura'),
    ('srf', 'Sin requisitos fiscales'),
    ('nde', 'No deducible'),
    ]


class Beneficiario(ClaseModelo2):
    beneficiario = models.CharField('Nombre', max_length= 100, blank=False, null=False)
    direccion = models.CharField('Dirección', max_length= 100, blank= True, null = True)
    rfc = models.CharField('RFC', max_length=13, blank=False, null=False)
    email = models.EmailField('Correo electrónico', blank=False, null=False)
    regimen = models.CharField('Régimen Fiscal', max_length= 100, blank= True, null = True)


    class Meta:
        verbose_name ='Beneficiario'
        verbose_name_plural = 'Beneficiarios'

    def __str__(self):
        return self.beneficiario


class SpyorEnc(ClaseModelo2):
    fecha_solicitud = models.DateField()
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    comentarios = models.TextField('Comentarios', blank=True, null=True, default="")
    imp_total = MoneyField('Importe Total', max_digits=14, decimal_places=2, blank=True, null=True,
                         default_currency="MXN", default=0)
    numero_cheque = models.CharField('Numero de cheque', max_length=20) 
    fecha_cheque = models.DateTimeField('Fecha del Cheque', blank=True, null=True)
    status = models.CharField('Status de la solicitud', max_length=30, default ="Capturada")

       

    def __str__(self):
        return '{}'.format(self.beneficiario)

    def save(self):
        #self.beneficiario = self.beneficiario.upper()
        super(SpyorEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Solicitudes"
        verbose_name="Encabezado Solicitud"

class SpyorDet(ClaseModelo2):
    solicitud = models.ForeignKey( SpyorEnc, on_delete=models.CASCADE )
    tipo_comprobante = models.CharField(max_length=20, choices= COMPROBANTE_CHOICES)
    no_facturasol = models.CharField('Folio', max_length=40, null=False, blank=False)
    fecha_compra = models.DateField(null=False, blank=False)
    importe = MoneyField('Importe con IVA incluido', max_digits=14, decimal_places=2, blank=False, null=False,
                         default_currency="MXN")
    descripcion = RichTextField('Descripción del gasto', blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    autoriza = models.BooleanField(default = False)
    fecha_autoriza = models.DateTimeField (blank=True, null=True)
    user_autoriza = models.CharField(max_length=20, blank=True, null=True)
    revisado = models.BooleanField(default = False)
    fecha_revisado = models.DateTimeField (blank=True, null=True)
    user_revisado = models.CharField(max_length=20, blank=True, null=True)
    
    imagen1 = models.ImageField(upload_to= 'media/', height_field=None, width_field=None, max_length=None, default = 'None/no-img.jpg', blank=True, null=True)
    imagen2 = models.ImageField(upload_to= 'media/', height_field=None, width_field=None, max_length=None, default = 'None/no-img.jpg')

    def __str__(self):
        return '{}'.format(self.no_facturasol)

    def save(self):
        # self.sub_total = float(float(int(self.cantidad)) * float(self.precio_prv))
        # self.total = self.sub_total - float(self.descuento)
        super(SpyorDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalle solicitudes"
        verbose_name="Detalle solicitud"   

@receiver(post_save, sender=SpyorDet)
def detalle_sol_guardar(sender,instance,**kwargs):
    solicitud_id = instance.solicitud.id
    

    enc = SpyorEnc.objects.get(pk=solicitud_id)
    if enc:
        xtotal = SpyorDet.objects \
            .filter(solicitud=solicitud_id) \
            .aggregate(xtotal=Sum('importe')) \
            .get('xtotal',0.00)
        
       
        
        enc.imp_total = xtotal
        
        enc.save()

@receiver(post_delete, sender=SpyorDet)
def detalle_sol_borrar(sender,instance,**kwargs):
    solicitud_id = instance.solicitud.id
    

    enc = SpyorEnc.objects.get(pk=solicitud_id)
    if enc:
        xtotal = SpyorDet.objects \
            .filter(solicitud=solicitud_id) \
            .aggregate(xtotal=Sum('importe')) \
            .get('xtotal',0.00)
        
       
        
        enc.imp_total = xtotal
        
        enc.save()