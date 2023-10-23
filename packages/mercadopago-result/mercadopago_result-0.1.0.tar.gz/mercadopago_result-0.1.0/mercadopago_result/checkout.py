from datetime import datetime
from pydantic import BaseModel
from pydantic import conlist
from pydantic import constr
from typing import Any
from typing import List
from typing import Literal
from typing import Optional
from enum import Enum

from mercadopago_result import constants
from mercadopago_result.common import AddressInformation
from mercadopago_result.constants import EmailAddressField
from mercadopago_result.item import Item
from mercadopago_result.user import BuyerInformation


ItemListField = conlist(Item, min_length=1)
""" The list of items for the checkout. """
RedirectUrl = constants.UrlString
""" URLs for requests' results. """
CheckoutAdditionalInformationField = constr(max_length=600)
""" Additional information for the checkout. """
CheckoutBranchIdField = str


class CheckoutAutoReturnOptions(Enum):
    APPROVED = "approved"
    ALL = "all"


CheckoutAutoReturnChoice = Literal[CheckoutAutoReturnOptions.APPROVED,
                                   CheckoutAutoReturnOptions.ALL]
""" If specified, your buyers will be redirected back to your site immediately
after completing the purchase.

approved - The redirection takes place only for approved payments.

all - The redirection takes place only for approved payments, forward
compatibility only if we change the default behavior.
"""
CheckoutExternalReferenceField = constr(max_length=256)
""" An external reference that can be used to synchronize with other payment
systems """
CheckoutPreferenceId = str
""" The Preference's ID
OBS.: should be a UUID but pydantic does not accept it. """
CheckoutMarketField = constr(max_length=256)
""" Origin of the payment.
No Idea what this means """
CheckoutMarketPlaceFeeField = float
""" Marketplace's fee charged by application owner.
Amount in local currency. """
CheckoutNotificationUrlField = constr(max_length=500)
""" It is a URL, but of course it will not be the same length as the others.
That would be too logical """
CheckoutOperationTypeField = Literal["regular_payment", "money_transfer"]
"""
regular_payment - Normal payment
money_transfer - Money request
"""
CheckoutProcessingModesField = list[Any]
""" No idea what this do, check the API if it has changed
https://api.mercadopago.com/checkout/preferences#options """
CheckoutSponsorIdField = int
""" Unique numeric ID to identify the sponsor. It is used to identify what
platform the checkout flow was initiated in. """
CheckoutSiteIdField = Literal["MLA",
                              "MLB",
                              "MLC",
                              "MLM",
                              "MLU",
                              "MCO",
                              "MPE"]
""" Possible values
MLA: Mercado Libre Argentina
MLB: Mercado Libre Brazil
MLC: Mercado Libre Chile
MLM: Mercado Libre México
MLU: Mercado Libre Uruguay
MCO: Mercado Libre Colombia
MPE: Mercado Libre Perú
"""


class CheckoutRedirectURLS(BaseModel):
    """Stores the urls for the request results. Depending on the result,
    it will call/redirect the client to a different constants.URL_STRING """

    success: RedirectUrl
    """Approved payment URL"""
    failure: RedirectUrl
    """Canceled payment URL"""
    pending: RedirectUrl
    """Pending payment URL"""


DifferentialPricingId = int


class DifferentialPricing(BaseModel):
    """ No idea what this does """
    id: DifferentialPricingId


PaymentMethodIdField = constr(max_length=256)
""" String with 256 characters """


class PaymentMethod(BaseModel):
    id: Optional[PaymentMethodIdField] = None


PaymentMethodsInstallmentsField = int
PaymentMethodsMethodIdList = list[PaymentMethod]
""" A list containing only payment methods ids """


class PaymentMethods(BaseModel):
    default_installments: Optional[PaymentMethodsInstallmentsField] = None
    """ Preferred number of credit card installments """
    default_payment_method_id: Optional[PaymentMethodIdField] = None
    """ Payment method to be preferred on the payments methods list """
    excluded_payment_methods: Optional[PaymentMethodsMethodIdList] = None
    """ Payment methods not allowed in payment process
    (except account_money) """
    installments: Optional[PaymentMethodsInstallmentsField] = None
    """ Maximum number of credit card installments to be accepted """


ShipmentInformationCostField = float
ShipmentInformationShippingMethodField = int
ShipmentInformationDimensionsField = str
ShipmentInformationFreeMethodId = int
ShipmentInformationFreeMethodsList = list[
    ShipmentInformationFreeMethodId]
""" No idea if this can be None or empty """
ShipmentInformationModeField = Literal["custom", "me2", "not_specified"]


class ShipmentInformation(BaseModel):
    cost: Optional[ShipmentInformationCostField] = None
    """ Shipment cost (mode:custom only) """
    default_shipping_method: Optional[
        ShipmentInformationShippingMethodField] = None
    """ Select default shipping method in checkout (mode:me2 only) """
    dimensions: Optional[ShipmentInformationDimensionsField] = None
    """ Dimensions of the shipment in cm x cm x cm, gr (mode:me2 only) """
    free_methods: Optional[ShipmentInformationFreeMethodsList] = None
    """ Offer a shipping method as free shipping (mode:me2 only) """
    free_shipping: Optional[bool] = None
    """ Free shipping for mode:custom """
    local_pickup: Optional[bool] = None
    """ The payer have the option to pick up the shipment in your store
    (mode:me2 only) """
    mode: Optional[ShipmentInformationModeField] = None
    """ Values:
    custom - Custom shipping
    me2 - MercadoEnvios
    not_specified - Shipping mode not specified """
    receiver_address: Optional[AddressInformation] = None


class Checkout(BaseModel):
    items: Optional[ItemListField] = None
    back_urls: Optional[CheckoutRedirectURLS] = None
    auto_return: Optional[CheckoutAutoReturnChoice] = None
    notification_url: Optional[CheckoutNotificationUrlField] = None
    """ URL where you'd like to receive a payment notification """
    additional_info: Optional[CheckoutAdditionalInformationField] = None
    binary_mode: Optional[bool] = False
    """ When set to true, the payment can only be approved or rejected.
    Otherwise in_process status is added. """
    branch_id: Optional[CheckoutBranchIdField] = None
    """ Represents the configured “external ID” that you registered in your
    Merchant Account from configuration’s menu in MercadoPago. The “external
    ID” allows you to divide your.
    """
    client_id: Optional[constants.ClientId] = None
    collector_id: Optional[constants.MercadoPagoSellerId] = None
    """ Your MercadoPago seller ID """
    date_created: Optional[datetime] = None
    differential_pricing: Optional[DifferentialPricing] = None
    """ Differential pricing configuration for this preference """
    expiration_date_from: Optional[datetime] = None
    """ Date since the preference will be active """
    expiration_date_to: Optional[datetime] = None
    """ Date when the preference will be expired """
    expires: Optional[bool] = False
    """ Boolean value that determines if a preference expire """
    external_reference: Optional[CheckoutExternalReferenceField] = None
    """ Reference you can synchronize with your payment system """
    id: Optional[CheckoutPreferenceId] = None
    """ Preference ID """
    init_point: Optional[constants.InitPointUrl] = None
    """ The URL that the client can access to finish the payment """
    marketplace: Optional[CheckoutMarketField] = None
    """ From where this was generated """
    marketplace_fee: Optional[CheckoutMarketPlaceFeeField] = 0
    """ Marketplace's fee charged by application owner. Default value: 0.
    amount in local currency """
    operation_type: Optional[CheckoutOperationTypeField] = None
    """ Operation data_type """
    payer: Optional[BuyerInformation] = None
    payment_methods: Optional[PaymentMethods] = None
    """ Set up payment methods to be excluded from the payment process """
    processing_modes: Optional[CheckoutProcessingModesField] = None
    """ This field represents the payment processing mode. It can be processed
    in two modes, aggregator (it uses a merchant account belonging to
    MercadoPago) or gateway (it uses your own merchant account id). Currently,
    we only support one mode at the same time. """
    sandbox_init_point: Optional[constants.InitPointUrl] = None
    """ Sandbox checkout access URL.
    OBS.: If you are using a test token then using this or the init_point will
    have the same effect. """
    shipments: Optional[ShipmentInformation] = None
    """ The API don't provide too much information about this field. """
    sponsor_id: Optional[CheckoutSponsorIdField] = None
    site_id: Optional[CheckoutSiteIdField] = None


CheckoutClientIdField = str
CheckoutConceptIdField = str
CheckoutCorporationIdField = str
CheckoutIntegratorIdField = str
CheckoutPlatformIdField = str
CheckoutShortenProcessingModesField = str
''' Processing mode'''
CheckoutShortenProductIdField = str
''' Unique ID used to identify the product. '''
CheckoutShortenPurposeField = str
CheckoutShortenShippingModeField = str
CheckoutShortenItemsField = List[str]


class CheckoutShorten(BaseModel):
    """ This is used for requesting the checkout list, for some reason
    MercadoPago chose to not return the same object as the other endpoints
    (╯°□°）╯︵ ┻━┻ """
    id: Optional[CheckoutPreferenceId] = None
    client_id: Optional[CheckoutClientIdField] = None
    collector_id: Optional[constants.MercadoPagoSellerId] = None
    ''' Unique ID used to identify the collector.
    It is the same as the Costumer ID. '''
    concept_id: Optional[CheckoutConceptIdField] = None
    ''' Unique ID used to identify the concept. '''
    corporation_id: Optional[CheckoutCorporationIdField] = None
    date_created: Optional[datetime] = None
    expiration_date_from: Optional[datetime] = None
    expiration_date_to: Optional[datetime] = None
    expires: Optional[bool] = None
    external_reference: Optional[CheckoutExternalReferenceField] = None
    integrator_id: Optional[CheckoutIntegratorIdField] = None
    items: Optional[CheckoutShortenItemsField] = None
    last_updated: Optional[datetime] = None
    live_mode: Optional[bool] = None
    ''' Indicates whether the Payment was made in a production environment or
    in a Test environment. If TRUE, then the chargeback will be processed in
    production mode. If FALSE, then the chargeback will be processed in sandbox
    mode. '''
    marketplace: Optional[CheckoutMarketField] = None
    operation_type: Optional[CheckoutOperationTypeField] = None
    payer_email: Optional[EmailAddressField] = None
    platform_id: Optional[CheckoutPlatformIdField] = None
    processing_modes: Optional[CheckoutShortenProcessingModesField] = None
    product_id: Optional[CheckoutShortenProductIdField] = None
    purpose: Optional[CheckoutShortenPurposeField] = None
    site_id: Optional[CheckoutSiteIdField] = None
    sponsor_id: Optional[CheckoutSponsorIdField] = None
    shipping_mode: Optional[CheckoutShortenShippingModeField] = None
