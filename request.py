import urllib2
import json

class OhRequest(object):
    HEADERS = { 'User-Agent' : 'OhPythonClient' }

    def body(self):
        return 'r=' + json.dumps({
            'EZMessage': {
                'action': self.action,
                'data': self.data,
            }
        })

    def request(self):
        return urllib2.Request(
            self.endpoint,
            self.body(),
            OhRequest.HEADERS
        )

class LoginRequest(OhRequest):
    def __init__(self, username, password):
        self.endpoint = 'https://api.optionshouse.com/m'
        self.action = 'auth.login'
        self.data = {
            'userName': username,
            'password': password,
        }

class LogoutRequest(OhRequest):
    def __init__(self, authToken):
        self.endpoint = 'https://api.optionshouse.com/m'
        self.action = 'auth.logout'
        self.data = {
            'authToken': authToken,
        }

class AccountInfoRequest(OhRequest):
    def __init__(self, authToken):
        self.endpoint = 'https://api.optionshouse.com/m'
        self.action = 'account.info'
        self.data = {
            'authToken': authToken,
        }

class AccountCashRequest(OhRequest):
    def __init__(self, authToken, account, **flags):
        self.endpoint = 'https://api.optionshouse.com/m'
        self.action = 'account.cash'
        self.data = {
            'authToken': authToken,
            'account': account,
        }

        if 'portfolio' in flags and flags['portfolio']:
            self.data['portfolio'] = True
        if 'historical' in flags and flags['historical']:
            self.data['historical'] = True
        if 'fastValues' in flags and flags['fastValues']:
            self.data['fastValues'] = True


class KeepAliveRequest(OhRequest):
    def __init__(self, authToken, account):
        self.endpoint = 'https://api.optionshouse.com/m'
        self.action = 'auth.keepAlive'
        self.data = {
            'authToken': authToken,
            'account': account,
        }

class ViewQuoteListRequest(OhRequest):
    def __init__(self, authToken, keys, **flags):
        self.endpoint = 'https://api.optionshouse.com/j'
        self.action = 'view.quote.list'
        self.data = {
            'authToken': authToken,
        }

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


class ViewSeriesRequest(OhRequest):
    def __init__(self, authToken, symbol, **flags):
        self.index = None
        self.endpoint = 'https://api.optionshouse.com/m'
        self.action = 'view.series'
        self.data = {
            'authToken': authToken,
            'symbol': symbol,
        }

        if 'quarterlies' in flags and flags['quarterlies']:
            self.data['quarterlies'] = True
        if 'weeklies' in flags and flags['weeklies']:
            self.data['weeklies'] = True

class AccountMarginJsonRequest(OhRequest):
    def __init__(self, authToken, account, order):
        self.endpoint = 'https://api.optionshouse.com/j'
        self.action = 'account.margin.json'
        self.data = {
            'authToken': authToken,
            'account': account,
            'order': order.toDict(),
        }

