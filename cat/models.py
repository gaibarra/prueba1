from django.db import models
from bases.models import ClaseModelo, ClaseModelo2

# Create your models here.
class Departamento(ClaseModelo):
    clavedepto = models.IntegerField(unique=True)
    departamento = models.CharField(max_length=200)


    def __str__(self):
        return self.departamento

    def save(self):
        self.departamento = self.departamento.upper()
        super(Departamento, self).save()

    class Meta:
        verbose_name_plural = "Departamentos"

class Funcionario(ClaseModelo2):
    codigo = models.CharField('Código', max_length=13, blank=False, null=False)
    nombre_funcionario = models.CharField('Nombre', max_length= 100, blank=False, null=False)
    clave_depto = models.IntegerField('Clave de Depto.', null=False)
    rfc = models.CharField('RFC', max_length=13, blank=False, null=False)
    curp = models.CharField('CURP', max_length=18, blank=False, null=False)
    fecha_ingreso = models.DateField('Fecha de ingreso', blank=False, null=False)
    email = models.EmailField('Correo electrónico', blank=False, null=False)
    grupo = models.CharField('Grupo', max_length=50, blank=True, null=True)
    imss = models.CharField('IMSS', max_length=11, blank=True, null=True)

    class Meta:
        verbose_name ='Funcionario'
        verbose_name_plural = 'Funcionarios y empleados'

    def __str__(self):
        return self.nombre_funcionario