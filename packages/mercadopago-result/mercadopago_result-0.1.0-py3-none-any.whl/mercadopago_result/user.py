from datetime import datetime
from pydantic import BaseModel
from pydantic import constr
from typing import Optional

from mercadopago_result.common import Phone
from mercadopago_result.constants import EmailAddressField


BuyerAddressStreetNameField = constr(max_length=256)
BuyerAddressStreetNumberField = int
BuyerAddressZipCodeField = constr(max_length=256)


class BuyerAddress(BaseModel):
    """ It seems like the same as the mercadopago_result.checkout.AddressInformation.
    But the API shows a different amount so seems better to make two separated
    classes. """
    street_name: Optional[BuyerAddressStreetNameField] = None
    street_number: Optional[BuyerAddressStreetNumberField] = None
    zip_code: Optional[BuyerAddressZipCodeField] = None


PersonalIdenticationNumberField = constr(max_length=256)
PersonalIdentificationTypeField = constr(max_length=256)


class PersonalIdentification(BaseModel):
    number: Optional[PersonalIdenticationNumberField] = None
    type: Optional[PersonalIdentificationTypeField] = None


BuyerNameField = constr(max_length=256)


class BuyerInformation(BaseModel):
    address: Optional[BuyerAddress] = None
    date_created: Optional[datetime] = None
    email: Optional[EmailAddressField] = None
    identification: Optional[PersonalIdentification] = None
    name: Optional[BuyerNameField] = None
    surname: Optional[BuyerNameField] = None
    phone: Optional[Phone] = None
