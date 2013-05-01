'''
Created on Apr 29, 2013

@author: pit
'''
from basededatos import *
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship, backref

class Suceso(Base):
    __tablename__ = "suceso"
    suceso_id= Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    fecha=Column(Date)
    urgencia=Column(Integer)
    impacto=Column(Integer)
    contador=Column(Integer)
    nivel=Column(String)
    clasificacion_id=Column(Integer, ForeignKey("clasificacion.clasificacion_id"))
    tipo_problema_id=Column(Integer,ForeignKey("tipo_problema.tipo_problema_id"))
    clasificacion=relationship("Clasificacion",backref=backref("suceso"))
    tipo_problema=relationship("TipoProblema",backref=backref("suceso"))
    
    