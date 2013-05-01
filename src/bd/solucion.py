'''
Created on Apr 29, 2013

@author: pit
'''
from basededatos import *
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship, backref
def __init__(self,tipo):
      self.tipo=tipo
class Solucion(Base):
    __tablename__ = "solucion"
    solucion_id= Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    fecha=Column(Date)
    tipo=Column(String)
    suceso_id=Column(Integer, ForeignKey("suceso.suceso_id"))
    departamento_id=Column(Integer,ForeignKey("departamento.departamento_id"))
    suceso=relationship("Suceso",backref=backref("solucion"))
    departamento=relationship("Departamento",backref=backref("solucion"))