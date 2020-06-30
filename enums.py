import enum

class AccountTypes(enum.Enum):
    Main = 'Main'
    Star = 'Star'
    Discount = 'Discount'
    Postpaid = 'Postpaid'
    Prepaid = 'Prepaid'


class OrderStatus(enum.Enum):
    Created = 'Created'
    Invoiced = 'Invoiced'
    Canceled = 'Canceled'
    Postponed = 'Postponed'


class Access_level(enum.Enum):
    Premium = 'Premium'
    Press = 'Press'
    Normal = 'Normal'


class Permissions(enum.Enum):
    IS_OWNER = 'IS_OWNER'
    IS_MEMBER = 'IS_MEMBER'
    ACCOUNT_ADD_PREMIUM = 'ACCOUNT_ADD_PREMIUM'
    ACCOUNT_EDIT_PREMIUM = 'ACCOUNT_EDIT_PREMIUM'
    ACCOUNT_DELETE_PREMIUM = 'ACCOUNT_DELETE_PREMIUM'
    ACCOUNT_GET_PREMIUM = 'ACCOUNT_GET_PREMIUM'

    TRANSACTION_ADD_PREMIUM = 'TRANSACTION_ADD_PREMIUM'
    TRANSACTION_DELETE_PREMIUM = 'TRANSACTION_DELETE_PREMIUM'
    TRANSACTION_GET_PREMIUM = 'TRANSACTION_GET_PREMIUM'

