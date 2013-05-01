'''
Created on Apr 22, 2013

@author: heli
'''

from basededatos import *
from sqlalchemy.orm import backref
from sqlalchemy.schema import ForeignKey


class Adjunto(Base):
  
  __tablename__ = "adjunto"
  
  adjunto_id = Column(Integer, primary_key=True)
  nombre = Column(String)
  localizacion= Column(String)
  
  #Comentar las opciones para los adjuntos (Documentadores)
  tipo_adjunto= Column(String)
  
    
  def altas(self):
    #????
    pass
  
  def descarga(self):
    #TODO: Return URL
    if self.localizacion[-1]!="/":
      return self.localizacion+"/"+self.nombre
    else:
      return self.localizacion+self.nombre
  
class RegistroAdjunto(Base):
  
  __tablename__="registro_adjunto"
  
  registro_adjunto_id= Column(Integer, primary_key=True)
  
  registro_id= Column(Integer)
  
  #Documentar Identificador de cada columna
  tabla_id= Column(String)
  
  #Documentar relacion con la clase 'Adjunto'
  adjunto_id=Column(Integer, ForeignKey ("adjunto.adjunto_id"))
  adjunto= relationship("Adjunto", backref=backref("registro_adjunto"))
  
