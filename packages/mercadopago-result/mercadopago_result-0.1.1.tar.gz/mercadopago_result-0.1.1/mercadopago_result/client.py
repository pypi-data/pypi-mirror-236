from datetime import datetime
from pydantic import BaseModel
from typing import List
from typing import Optional
from typing import Union

from mercadopago_result.common import AddressIdField
from mercadopago_result.common import AddressInformation
from mercadopago_result.common import CardIdField
from mercadopago_result.common import Card
from mercadopago_result.common import Phone
from mercadopago_result.constants import ClientId
from mercadopago_result.constants import EmailAddressField


ClientIdentificationTypeField = str
ClientIdenfiticationNumberField = Union[int, str]
''' In the API specify as a number, but the example sends as a string and the
response returns as a number'''


class ClientIdenfitication(BaseModel):
    type: Optional[ClientIdentificationTypeField] = None
    number: Optional[ClientIdenfiticationNumberField] = None


MetadataSourceSyncField = str


class ClientMetadata(BaseModel):
    source_sync: MetadataSourceSyncField


ClientIdField = ClientId
ClientNameField = str
ClientDescriptionField = str
ClientCardListField = List[Card]
ClientAddressesField = List[AddressInformation]
ClientLiveMode = bool
''' Whether the customers will be in sandbox or in production mode. '''


class Client(BaseModel):
    id: Optional[ClientIdField] = None
    email: Optional[EmailAddressField] = None
    first_name: Optional[ClientNameField] = None
    last_name: Optional[ClientNameField] = None
    phone: Optional[Phone] = None
    identification: Optional[ClientIdenfitication] = None
    address: Optional[AddressInformation] = None
    date_registered: Optional[datetime] = None
    description: Optional[ClientDescriptionField] = None
    date_created: Optional[datetime] = None
    date_last_updated: Optional[datetime] = None
    metadata: Optional[ClientMetadata] = None
    default_card: Optional[CardIdField] = None
    default_address: Optional[AddressIdField] = None
    cards: Optional[ClientCardListField] = None
    addresses: Optional[ClientAddressesField] = None
