'''
Created on Apr 22, 2013

@author: pit
'''
from basededatos import *
from sqlalchemy.schema import Column

class TipoProblema(Base):
    __tablename__ = "tipo_problema"
    tipo_problema_id= Column(Integer, primary_key=True)
    tipo = Column(String)
    
    
      
    def alta(self):
        pass