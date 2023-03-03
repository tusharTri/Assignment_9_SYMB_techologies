
from database import Base, engine
from sqlalchemy import DateTime, Text, Integer,Column, BigInteger, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

def create_tables():
    Base.metadata.create_all(engine)

class CountryModel(Base):
    __tablename__='countries'
    # __table_args__ = {'extend_existing': True}
    id=Column(Integer,  nullable=False, primary_key=True) 
    name=Column(Text,  nullable=False) 
    cca=Column(Text,  nullable=False)
    currency_code=Column(Text,  nullable=False)
    currency=Column(Text,  nullable=False) 
    capital=Column(Text,  nullable=False)
    region=Column(Text,  nullable=False) 
    subregion=Column(Text,  nullable=False) 
    area =Column(BigInteger,  nullable=False)
    map_url=Column(Text,  nullable=False) 
    population=Column(BigInteger,  nullable=False)
    flag_url =Column(Text,  nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    neighbours_rel=relationship("CountryNeighbour", back_populates="countries_rel") 
    

    
class CountryNeighbour(Base):
    __tablename__='country_neighbours'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, nullable=False, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    neighbour_country_id = Column(Text,  nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    countries_rel=relationship("CountryModel",back_populates="neighbours_rel")