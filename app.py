from fastapi import FastAPI,status, Response
import models 
from base_models import CountryModel, CountryNeighbour
from typing import List,Union
from database import SessionLocal, engine
from sqlalchemy.orm import Session
app=FastAPI()
from uvicorn import logging


db = SessionLocal()
# uvicorn app:app --reload

@app.get('/country',status_code=status.HTTP_200_OK)
def show_all_country(page: int = 1,limit: int=10,name: Union[str, None] = None,region: Union[str, None] = None,
                     subregion: Union[str, None] = None,sort_by: Union[str, None] = None):
    sort_query = '(models.CountryModel.'
    search_query=''
    if sort_by == 'a_toz':sort_query+= 'name)'
    elif sort_by == 'z_toa':sort_query += 'name.desc())'
    elif sort_by == 'population_high_to_low':sort_query += 'population.desc())'
    elif sort_by == 'population_low_to_high':sort_query += 'population)'
    elif sort_by == 'area_high_to_low':sort_query += 'area.desc())'
    elif sort_by == 'area_low_to_high':sort_query += 'area)'
    else: sort_query +='id)'
    
    if name:search_query += 'name=name,'
    if region:search_query += 'region=region,'
    if subregion:search_query += 'subregion=sub_region'
    # .filter_by({name}{region}{subregion})
    final_query = 'db.query(models.CountryModel)'
    
    if search_query: final_query += f'.filter_by({search_query})' 
    if sort_query:   final_query += f'.order_by{sort_query}'
    off=limit*(page-1)
    final_query += f'.offset({off}).limit({limit}).all()'
    countries = eval(final_query)
    
    listcountry=[]
    for country in countries:
            obj={c.name: getattr(country, c.name) for c in country.__table__.columns}
            listcountry.append(obj)
    total=len(db.query(models.CountryModel).all())
    pages=(total//limit)+1
    list={'List' : listcountry}
    return {'message': 'Country list','data': list,'has_next': page<pages,
    'has_prev': page>1,'page':page,'pages':pages,'per_page':limit,'total':total}
    
        



@app.get('/country/{id}',status_code=status.HTTP_200_OK)
def countryById(id,response:Response):
    try:
        country = db.query(models.CountryModel).filter(models.CountryModel.id==id).first()
        obj={c.name: getattr(country, c.name) for c in country.__table__.columns}
        detcountry={'country':obj}
        return {'message': 'Country detail','data': detcountry}                    
    except:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"message": "Country not found","data": {}}


@app.get('/country/{id}/neighbour',status_code=status.HTTP_200_OK)
def neighbour(id, response=Response):
    if( db.query(models.CountryModel).filter(models.CountryModel.id==id).first()): 
        
        neighbour=db.query(models.CountryModel).join(models.CountryNeighbour, models.CountryModel.id == models.CountryNeighbour.country_id)\
                                          .filter(models.CountryNeighbour.neighbour_country_id == id).all()
        if(neighbour):
            listcountry=[]
            for country in neighbour:
                obj={c.name: getattr(country, c.name) for c in country.__table__.columns}
                listcountry.append(obj)
            country={'country':listcountry}
            return {'message': 'Neighbours','data': country}      
        else:
            return {"message": "Country neighnbours","data" : {"list": []}}
              
    else:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"message": "Country not found","data": {}}



@app.post('/country',response_model=CountryModel,status_code=status.HTTP_201_CREATED )
async def new_country(country:CountryModel):
    
    data=country.dict()
    entry = models.CountryModel(id=data['id'], name=data['name'], cca=data['cca'],
                    currency_code=data['currency_code'], currency=data['currency'], capital=data['capital'],
                    region=data['region'], subregion=data['subregion'],
                    area=data['area'],
                    map_url=data['map_url'], 
                    population=data['population'],
                    flag_url=data['flag_url'])
    
    db.add(entry)
    db.commit()
    return 'recieved'