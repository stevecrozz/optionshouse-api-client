import urllib2
import json
from request import *

class Session(object):

    def __init__(self, username, password):
        """
        Create a Session object. Username and password are both required
        parameters
        """
        self.username = username
        self.password = password
        self.state = 'closed'
        self.authToken = None

    def open(self):
        """
        Open the session by logging into the optionshouse API. Optionshouse
        returns an authToken which is stored in this Session object for future
        use.
        """

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
        """
        Close the session by logging out of the optionshouse API. The authToken
        will be invalidated and cleared from the session.
        """

        oh_res = self.issue_request(
            LogoutRequest(self.authToken))

        if 'logout' in oh_res:
            self.authToken = None
            self.state = 'closed'
        else:
            print oh_res

    def keepalive(self, account):
        """
        Without making any requests, sessions expire. Calling this method
        periodically will keep this from happening.
        """

        return self.issue_request(
            KeepAliveRequest(self.authToken, account))

    def account_info(self):
        """
        Get information about accounts associated with login provided
        """

        return self.issue_request(
            AccountInfoRequest(self.authToken))

    def account_cash(self, account, **kwargs):
        """
        Get all the available financial information about the provided account
        """

        return self.issue_request(
            AccountCashRequest(self.authToken, account, **kwargs))

    def quote(self, keys, **kwargs):
        """
        For a given list of keys, get a list of quote information. Optionally,
        you may provide additional boolean flags to augment the response with
        more information:

        addExtended: include extended hours data
        addStockDetails: include additional details
        addFundamentalDetails: include fundamental details
        """

        return self.issue_request(
            ViewQuoteListRequest(self.authToken, keys, **kwargs))

    def options_list(self, symbol, **kwargs):
        """
        Given the provided underlying symbol, get a list of available options.
        You may optionally include the following boolean flags for more info:

        quarterlies: include quarterly options
        weeklies: include weekly options
        """

        return self.issue_request(
            ViewSeriesRequest(self.authToken, symbol, **kwargs))

    def preview_order(self, account, order):
        """
        Given an account and an Order object, preview details about the order
        and the effect it will have on your account
        """

        return self.issue_request(
            AccountMarginJsonRequest(self.authToken, account, order))

    def place_order(self, account, order):
        """
        Given an account and an Order object, actually place the order
        """

        return self.issue_request(
            OrderCreateJsonRequest(self.authToken, account, order))

    def modify_order(self, account, order, old_order_id):
        """
        For the given account, ask optionshouse to replace an existing order
        with a new one. The exisitng order must be specified using the
        old_order_id argument.
        """

        order.modify(old_order_id)

        return self.issue_request(
            OrderModifyJsonRequest(self.authToken, account, order))

    def cancel_order(self, account, order_id):
        """
        Given an account and an order_id, ask optionshouse to cancel the order
        """

        return self.issue_request(
            OrderCancelJsonRequest(self.authToken, account, order_id))

    def list_orders(self, account, **kwargs):
        """
        Get a list of current or archived orders for the given account.

        The keyword argument 'master_order_view' must be provided and it must
        be 'current' or 'archived'

        You may optionally filter the results by providing a 'key' keyword
        argument and pagination is controlled using 'page', 'page_count' and
        'page_size' keyword arguments.
        """

        return self.issue_request(
            MasterAccountOrdersRequest(self.authToken, account, **kwargs))

    def account_positions(self, account):
        """
        Query all the positions held by the given account including current
        price and cost basis information
        """

        return self.issue_request(
            AccountPositionsRequest(self.authToken, account))

    def account_activity(self, account, **kwargs):
        """
        Get a list of activity for the given account

        Available filters are:
        sDate: String mm/dd/yyyy - start date
        eDate: String mm/dd/yyyy - end date
        symbol: underlying ticker symbol

        Pagination is controlled with:
        page, maxPage, size and totalCount
        """

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

