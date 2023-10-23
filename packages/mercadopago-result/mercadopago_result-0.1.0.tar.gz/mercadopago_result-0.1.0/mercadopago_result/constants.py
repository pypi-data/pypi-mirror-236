from pydantic import constr
from enum import Enum


UrlString = constr(max_length=600)
""" Type: str. Max length: 600. Represents the URL field for requests. """
ClientId = str
""" Application owner ID that use MercadoLibre API. """
MercadoPagoSellerId = int
""" MercadoPago seller ID """
InitPointUrl = str
""" Has no size specification... """
EmailAddressField = constr(max_length=256)
""" Email address max size 256 """


# https://api.mercadopago.com/currencies/#json
class ValidCurrencies(str, Enum):
    BRL = "BRL"
    ARS = "ARS"
    BOB = "BOB"
    CLF = "CLF"
    CLP = "CLP"
    COP = "COP"
    CRC = "CRC"
    CUC = "CUC"
    CUP = "CUP"
    DOP = "DOP"
    EUR = "EUR"
    GTQ = "GTQ"
    HNL = "HNL"
    MXN = "MXN"
    NIO = "NIO"
    PAB = "PAB"
    PEN = "PEN"
    PYG = "PYG"
    USD = "USD"
    UYU = "UYU"
    VEF = "VEF"
    VES = "VES"
