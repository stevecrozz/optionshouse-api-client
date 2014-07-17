import sys, json

if sys.version_info[0] < 3:
    from urllib2 import Request
else:
    from urllib.request import Request

class OhRequest(object):
    """
    Abstract request class. All other request classes are subclasses of this
    one.
    """

    HEADERS = { 'User-Agent' : 'OhPythonClient' }

    def __init__(self):
        self.endpoint = self.ENDPOINT
        self.action = self.ACTION
        self.data = {}

    def body(self):
        """
        Get the text of the request body that should be sent to optionshouse.
        Here we have hardcoded r= which tells optionshouse we will be passing a
        JSON request and we expect a JSON response.
        """

        return 'r=' + json.dumps({
            'EZMessage': {
                'action': self.action,
                'data': self.data,
            }
        })

    def request(self):
        """
        Get a Request object representation of this request
        """

        return Request(
            self.endpoint,
            self.body(),
            OhRequest.HEADERS
        )

    @classmethod
    def requires_auth_token(self, fn):
        """
        Decorator adds authToken as an argument
        """

        def wrapper(self, *args, **kwargs):
            args = list(args)
            authToken = args.pop(0)
            fn(self, *args, **kwargs)
            self.data['authToken'] = authToken
            self.requires_auth_token = True

        return wrapper

    @classmethod
    def requires_account(self, fn):
        """
        Decorator adds account as an argument
        """

        def wrapper(self, *args, **kwargs):
            args = list(args)
            account = args.pop(0)
            fn(self, *args, **kwargs)

            if self.__class__.__name__ == "MasterAccountOrdersRequest":
                # OptionsHouse calls this an account_id for this one request
                # and just account for all the others. Why would you do that,
                # OptionsHouse?
                self.data['account_id'] = account
            else:
                self.data['account'] = account

            self.requires_account = True

        return wrapper

class LoginRequest(OhRequest):

    ENDPOINT = 'https://api.optionshouse.com/m'
    ACTION = 'auth.login'

    def __init__(self, username, password):
        super(LoginRequest, self).__init__()
        self.data['userName'] = username
        self.data['password'] = password

class LogoutRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/m'
    ACTION = 'auth.logout'

    @OhRequest.requires_auth_token
    def __init__(self):
        super(LogoutRequest, self).__init__()

class AccountInfoRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/m'
    ACTION = 'account.info'

    @OhRequest.requires_auth_token
    def __init__(self):
        super(AccountInfoRequest, self).__init__()

class AccountCashRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/m'
    ACTION = 'account.cash'

    @OhRequest.requires_auth_token
    @OhRequest.requires_account
    def __init__(self, **flags):
        super(AccountCashRequest, self).__init__()

        if 'portfolio' in flags and flags['portfolio']:
            self.data['portfolio'] = True
        if 'historical' in flags and flags['historical']:
            self.data['historical'] = True
        if 'fastValues' in flags and flags['fastValues']:
            self.data['fastValues'] = True


class KeepAliveRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/m'
    ACTION = 'auth.keepAlive'

    @OhRequest.requires_auth_token
    @OhRequest.requires_account
    def __init__(self):
        super(KeepAliveRequest, self).__init__()

class ViewQuoteListRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/j'
    ACTION = 'view.quote.list'

    @OhRequest.requires_auth_token
    def __init__(self, keys, **flags):
        super(ViewQuoteListRequest, self).__init__()

        if len(keys) == 0:
            "Can't proceed without any keys"
            return

        self.data['key'] = []

        for key in keys:
            # Assume anything without colons is a plain old stock
            if key.find(":") == -1:
                key = "%s:::S" % key

            self.data['key'].append(key)

        if 'extended' in flags and flags['extended']:
            self.data['addExtended'] = self.data['key']
        if 'stock_details' in flags and flags['stock_details']:
            self.data['addStockDetails'] = self.data['key']
        if 'fundamental_details' in flags and flags['fundamental_details']:
            self.data['addFundamentalDetails'] = self.data['key']

class MarketStatusRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/m'
    ACTION = 'view.quote.list'

    @OhRequest.requires_auth_token
    def __init__(self, **flags):
        super(MarketStatusRequest, self).__init__()

        self.data['key'] = ['MARKETSTATUS']

class ViewSeriesRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/m'
    ACTION = 'view.series'

    @OhRequest.requires_auth_token
    def __init__(self, symbol, **flags):
        super(ViewSeriesRequest, self).__init__()
        self.index = None
        self.data['symbol'] = symbol

        if 'quarterlies' in flags and flags['quarterlies']:
            self.data['quarterlies'] = True
        if 'weeklies' in flags and flags['weeklies']:
            self.data['weeklies'] = True

class AccountMarginJsonRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/j'
    ACTION = 'account.margin.json'

    @OhRequest.requires_auth_token
    @OhRequest.requires_account
    def __init__(self, order):
        super(AccountMarginJsonRequest, self).__init__()
        self.data['order'] = order.toDict()

class OrderCreateJsonRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/j'
    ACTION = 'order.create.json'

    @OhRequest.requires_auth_token
    @OhRequest.requires_account
    def __init__(self, order):
        super(OrderCreateJsonRequest, self).__init__()
        self.data['order'] = order.toDict()

class OrderModifyJsonRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/j'
    ACTION = 'order.modify.json'

    @OhRequest.requires_auth_token
    @OhRequest.requires_account
    def __init__(self, order):
        super(OrderModifyJsonRequest, self).__init__()
        self.data['order'] = order.toDict()

class OrderCancelJsonRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/j'
    ACTION = 'order.cancel.json'

    @OhRequest.requires_auth_token
    @OhRequest.requires_account
    def __init__(self, order_id):
        super(OrderCancelJsonRequest, self).__init__()
        self.data['order_id'] = order_id

class MasterAccountOrdersRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/j'
    ACTION = 'master.account.orders'

    @OhRequest.requires_auth_token
    @OhRequest.requires_account
    def __init__(self, **flags):
        super(MasterAccountOrdersRequest, self).__init__()
        self.data['master_order'] = {
            'master_order_view': 'current',
        }

        if 'symbol' in flags:
            self.data['symbol'] = flags['symbol']
        if 'archived' in flags and flags['archived']:
            self.data['master_order']['master_order_view'] = 'archived'
        if 'page' in flags:
            self.data['master_order']['page'] = flags['page']
        if 'page_count' in flags:
            self.data['master_order']['page_count'] = flags['page_count']
        if 'page_size' in flags:
            self.data['master_order']['page_size'] = flags['page_size']

class AccountPositionsRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/m'
    ACTION = 'account.positions'

    @OhRequest.requires_auth_token
    @OhRequest.requires_account
    def __init__(self):
        super(AccountPositionsRequest, self).__init__()

class AccountActivityRequest(OhRequest):
    ENDPOINT = 'https://api.optionshouse.com/m'
    ACTION = 'account.activity'

    @OhRequest.requires_auth_token
    @OhRequest.requires_account
    def __init__(self, **kwargs):
        super(AccountActivityRequest, self).__init__()

        if 'page' in kwargs:
            self.data['page'] = kwargs['page']
        if 'maxPage' in kwargs:
            self.data['maxPage'] = kwargs['maxPage']
        if 'size' in kwargs:
            self.data['size'] = kwargs['size']
        if 'totalCount' in kwargs:
            self.data['totalCount'] = kwargs['totalCount']
        if 'sDate' in kwargs:
            self.data['sDate'] = kwargs['sDate']
        if 'eDate' in kwargs:
            self.data['eDate'] = kwargs['eDate']
        if 'symbol' in kwargs:
            self.data['symbol'] = kwargs['symbol']

