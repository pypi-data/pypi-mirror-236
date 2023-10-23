from pydantic import BaseModel
from pydantic import constr
from typing import Optional


PhoneAreaCodeField = constr(max_length=256)
PhoneNumberField = constr(max_length=256)


class Phone(BaseModel):
    area_code: Optional[PhoneAreaCodeField] = None
    number: Optional[PhoneNumberField] = None


CityNameField = str


class CityInformation(BaseModel):
    name: Optional[CityNameField] = None


AddressApartmentField = constr(max_length=256)
AddressFloorField = constr(max_length=256)
AddressStreetNameField = constr(max_length=256)
AddressStreetNumberField = int
AddressZipCodeField = constr(max_length=256)
AddressIdField = str


class AddressInformation(BaseModel):
    id: Optional[AddressIdField] = None
    apartment: Optional[AddressApartmentField] = None
    floor: Optional[AddressFloorField] = None
    street_name: Optional[AddressStreetNameField] = None
    street_number: Optional[AddressStreetNumberField] = None
    zip_code: Optional[AddressZipCodeField] = None
    city: Optional[CityInformation] = None


CardIdField = str


class Card(BaseModel):
    id: CityNameField
