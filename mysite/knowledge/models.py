from django.db import models
from django.forms import ModelForm
from django.template.defaultfilters import default
from django.utils.datetime_safe import datetime
from django.db.models.base import Model

class Clasificacion(models.Model):
  nombre = models.CharField(max_length=50)
    
  def __unicode__(self):
    return self.nombre

class Departamento(models.Model):
  nombre = models.CharField(max_length=50)
  descripcion= models.CharField(max_length=50)
  def __unicode__(self):
    return self.nombre
class TipoProblema(models.Model):
    tipo = models.CharField(max_length=50)
    def __unicode__(self):
      return self.tipo

class Adjunto(models.Model):
  nombre = models.CharField(max_length=50)
  localizacion=models.FileField(upload_to='./archivos', blank = True)
  #Comentar las opciones para los adjuntos (Documentadores)
  tipo_adjunto= models.CharField(max_length=50)
  def __unicode__(self):
    return self.nombre
class RegistroAdjunto(models.Model):
  registro_id= models.IntegerField(max_length=50)
  #Documentar Identificador de cada columna
  tabla=models.CharField(max_length=50)
  adjuntos=models.ForeignKey(Adjunto)
  def __unicode__(self):
    return 'es un archivo de'+self.tabla+ 'del registro'+str(self.registro_id) 

class Suceso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha=models.DateField("Fecha: dd/mm/aaaa",default=datetime.now())
    urgencia=models.IntegerField(max_length=50,choices=((1,1),(2,2),(3,3)))
    impacto=models.IntegerField(max_length=50,choices=((1,1),(2,2),(3,3)))
    contador=models.IntegerField(max_length=50,default=0)
    nivel=models.CharField(max_length=50)     
    clasificacion=models.ForeignKey(Clasificacion)
    tipo_problema=models.ForeignKey(TipoProblema)
    def __unicode__(self):
      return self.nombre
class Solucion(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=50)
    fecha=models.DateField()
    tipo=models.CharField(max_length=50)
    sucesos=models.ForeignKey(Suceso)
    departamentos=models.ForeignKey(Departamento)
    def __unicode__(self):
      self.nombre

class SucesoForm(ModelForm):
  class Meta:
    model= Suceso
    exclude=['fecha','nivel']
    #fields=['nombre','descripcion']
class AdjuntoForm(ModelForm):
  class Meta:
    model=Adjunto