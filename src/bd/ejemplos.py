'''
Created on Apr 30, 2013

@author: pit
'''
import initDataBase
from suceso import Suceso
from clasificacion import Clasificacion
from tipoproblema import TipoProblema
from basededatos import session

suceso=Suceso(nombre="no enciende")
tipo_problema=session.query(TipoProblema).filter(TipoProblema.tipo=="hardware").first()

suceso2=Suceso(nombre="audio no funka",descripcion="no funciona y los controladores estan instalados")
tipo_problema.suceso=[suceso,suceso2]

session.add(tipo_problema)
session.commit()
session.commit()

