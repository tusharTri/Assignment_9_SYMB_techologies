from pydantic import BaseModel


class CountryModel(BaseModel):
    id: int
    name: str
    cca: str
    currency_code: str
    currency: str
    capital: str
    region: str
    subregion: str
    area: int
    map_url: str
    population: int
    flag_url: str
    # created_at: str
    # updated_at: str

    
    class Config:
        orm_mode = True


class CountryNeighbour(BaseModel):
    id: int
    country_id: int
    neighbour_country_id: str
    # created_at: str
    # updated_at: str

    class Config:
        orm_mode = True
