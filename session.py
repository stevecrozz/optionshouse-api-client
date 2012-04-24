import urllib2
import json
from request import *

class Session(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.state = 'closed'
        self.authToken = None

    def open(self):
        oh_res = self.issue_request(
            LoginRequest(self.username, self.password))

        if oh_res == None:
            "raise some exception"
            return

        if 'authToken' in oh_res:
            self.authToken = oh_res['authToken']
            self.state = 'open'
        else:
            print oh_res

    def close(self):
        oh_res = self.issue_request(
            LogoutRequest(self.authToken))

        if 'logout' in oh_res:
            self.authToken = None
            self.state = 'closed'
        else:
            print oh_res

    def keepalive(self, account):
        return self.issue_request(
            KeepAliveRequest(self.authToken, account))

    def account_info(self):
        return self.issue_request(
            AccountInfoRequest(self.authToken))

    def account_cash(self, account, **kwargs):
        return self.issue_request(
            AccountCashRequest(self.authToken, account, **kwargs))

    def quote(self, keys, **kwargs):
        return self.issue_request(
            ViewQuoteListRequest(self.authToken, keys, **kwargs))

    def options_list(self, symbol, **kwargs):
        return self.issue_request(
            ViewSeriesRequest(self.authToken, symbol, **kwargs))

    def preview_order(self, account, order):
        return self.issue_request(
            AccountMarginJsonRequest(self.authToken, account, order))

    def place_order(self, account, order):
        return self.issue_request(
            OrderCreateJsonRequest(self.authToken, account, order))

    def modify_order(self, account, order):
        return self.issue_request(
            OrderModifyJsonRequest(self.authToken, account, order))

    def cancel_order(self, account, order_id):
        return self.issue_request(
            OrderCancelJsonRequest(self.authToken, account, order_id))

    def list_orders(self, account, **kwargs):
        return self.issue_request(
            MasterAccountOrdersRequest(self.authToken, account, **kwargs))

    def account_positions(self, account):
        return self.issue_request(
            AccountPositionsRequest(self.authToken, account))

    def account_activity(self, account, **kwargs):
        return self.issue_request(
            AccountActivityRequest(self.authToken, account, **kwargs))

    def issue_request(self, ohreq):
        try:
            oh_res = urllib2.urlopen(ohreq.request())
        except urllib2.HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except urllib2.URLError, e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        else:
            return self.parse_response(oh_res)

    def parse_response(self, ohres):
        response = json.loads(ohres.read())['EZMessage']

        if 'errors' in response:
            print response['errors']
        else:
            return response['data']

