'''
Created on Apr 22, 2013

@author: heli
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
motor=create_engine("sqlite:///datos.db", echo=True)
Base=declarative_base()

