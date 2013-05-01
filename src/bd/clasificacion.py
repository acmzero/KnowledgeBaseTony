'''
Created on Apr 22, 2013

@author: pit
'''
from basededatos import *
from sqlalchemy.schema import Column

class Clasificacion(Base):
    __tablename__ = "clasificacion"
    clasificacion_id= Column(Integer, primary_key=True)
    nombre = Column(String)
    
    
    
    
    def alta(self):
        pass