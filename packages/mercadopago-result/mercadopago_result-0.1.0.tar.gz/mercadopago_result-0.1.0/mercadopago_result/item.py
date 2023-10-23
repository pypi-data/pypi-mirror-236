from pydantic import BaseModel
from pydantic import Field
from pydantic import constr
from typing import Optional

from mercadopago_result import constants


ItemTitleField = constr(max_length=256)
"""Type: str. Max length: 256. Represents the title field of an item."""

ItemDescriptionField = constr(max_length=256)
"""Type: str. Max length: 256. Represents the description field of an item."""

ItemIdField = constr(max_length=256)
"""Type: str. Max length: 256. Represents the ID field of an item."""

ItemQuantityField = int
"""Type: int. Represents the quantity field of an item."""

ItemUrlField = constants.UrlString
"""Type: str. Max length: 600. Represents the URL field of an item."""

ItemCategoryIdField = constr(max_length=256)
"""Type: str. Max length: 256. Represents the category ID field of an item."""

CurrencyId = constr(max_length=3)
"""Type: str. Max length: 3. Represents the currency ID field."""

ItemUnitPriceField = float
"""Type: float. Represents the unit price field of an item."""


class Item(BaseModel):
    '''Used to describe an item/product'''

    quantity: ItemQuantityField = Field(None, ge=1)
    unit_price: ItemUnitPriceField = Field(None, gt=0.0)
    title: Optional[ItemTitleField] = None

    id: Optional[ItemIdField] = None
    """ the API says it must have, but example does not include it """
    currency_id: Optional[CurrencyId] = None
    category_id: Optional[ItemCategoryIdField] = None
    description: Optional[ItemDescriptionField] = None
    picture_url: Optional[ItemUrlField] = None
