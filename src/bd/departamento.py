'''
Created on Apr 22, 2013

@author: pit
'''
from basededatos import *
from sqlalchemy.schema import Column

class Departamento(Base):
    __tablename__ = "departamento"
    departamento_id= Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion= Column(String)
    
    
    def alta(self):
        pass