from django.db import models

# Create your models here.
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
    

class Suceso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha=models.CharField(max_length=50)
    urgencia=models.IntegerField(max_length=50)
    impacto=models.IntegerField(max_length=50)
    contador=models.IntegerField(max_length=50)
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


     