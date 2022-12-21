# !/usr/bin/env python
# *- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, Float, CHAR, VARCHAR, DATETIME, FLOAT, DateTime, Date

from config import *

config = Config()
Base = declarative_base()

class DerivFuel(Base):
    __tablename__ = 'tbl_deriv'
    
    cod_id     = Column(Integer,primary_key=True)
    year_month = Column(Date)
    uf         = Column(CHAR(255))
    product    = Column(CHAR(255))
    unit       = Column(CHAR(255))
    volume     = Column(Float)
    created_at = Column(DATETIME)
    
class DieselFuel(Base):
    __tablename__ = 'tbl_diesel'
    
    cod_id     = Column(Integer,primary_key=True)
    year_month = Column(Date)
    uf         = Column(CHAR(255))
    product    = Column(CHAR(255))
    unit       = Column(CHAR(255))
    volume     = Column(Float)
    created_at = Column(DATETIME)
    
engine = create_engine(config.string_engine.format(**config.config_banco), echo=True)

try:
    Base.metadata.create_all(engine)
except:
    engine = create_engine(config.string_engine)
    Base.metadata.create_all(engine)

