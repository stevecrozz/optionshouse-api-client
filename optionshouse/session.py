import json, time, sys

if sys.version_info[0] < 3:
    from urllib2 import urlopen, HTTPError, URLError
else:
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError

from request import *

class OhRequestException(Exception):
    """
    This exception should be raised when the HTTP response from optionshouse
    includes errors
    """

    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return repr(self.errors)

class OhUnknownException(Exception):
    """
    This exception should be raised when some improper condition has been
    reached and no further information is available
    """

    pass

class OhConnectionException(Exception):
    """
    This exception should be raised when the server returns an error-level HTTP
    response code or the server could not be reached at all
    """

    def __str__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


class Session(object):
    """
    A Session object is the simplest way to make use of this library. When you
    open a Session object using your login credentials, the Sessoin object
    stores a copy of the authToken returned by optionshouse and uses the
    authToken for all subsequent requests.

    You may keep your Session from expiring by calling #keepalive every so
    often. There are helper methods on Session objects for every documented
    optionshouse API call. Each successful helper method will return the data
    portion of the JSON response from optionshouse.

    Methods that take an 'account' parameter need to be given an account_id
    (which is different from an account number). You can get your account_id by
    checking the response from #account_info.

    Exampe:
    s = Session('myusername', 'mypassword')
    s.open()
    s.quote("GS")
    s.close()
    """

    TIME_BETWEEN_REQUESTS = 1

    def __init__(self, username, password):
        """
        Create a Session object. Username and password are both required
        parameters
        """
        self.username = username
        self.password = password
        self.state = 'closed'
        self.authToken = None
        self.last_request_time = None

    def wait(self, seconds_to_wait):
        """
        __Wait is called internally when the session has been asked to make a
        request within a short time of another request. This is a protection
        mechanism to avoid violating the terms of the optionshouse API
        agreement. The documentation says no more than 1 request per second is
        allowed.
        """

        time.sleep(seconds_to_wait)

    def open(self):
        """
        Open the session by logging into the optionshouse API. Optionshouse
        returns an authToken which is stored in this Session object for future
        use.
        """

        oh_res = self.request(
            LoginRequest(self.username, self.password))

        if oh_res == None:
            "raise some exception"
            return

        if 'authToken' in oh_res:
            self.authToken = oh_res['authToken']
            self.state = 'open'
        else:
            raise OhUnkownException()

    def close(self):
        """
        Close the session by logging out of the optionshouse API. The authToken
        will be invalidated and cleared from the session.
        """

        oh_res = self.request(
            LogoutRequest(self.authToken))

        if 'logout' in oh_res:
            self.authToken = None
            self.state = 'closed'
        else:
            raise OhUnkownException()

    def keepalive(self, account):
        """
        Without making any requests, sessions expire. Calling this method
        periodically will keep this from happening.
        """

        return self.request(
            KeepAliveRequest(self.authToken, account))

    def account_info(self):
        """
        Get information about accounts associated with login provided
        """

        return self.request(
            AccountInfoRequest(self.authToken))

    def account_cash(self, account, **kwargs):
        """
        Get all the available financial information about the provided account
        """

        return self.request(
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

        return self.request(
            ViewQuoteListRequest(self.authToken, keys, **kwargs))

    def market_status(self):
        """
        Return whether or not the market is closed
        """
        return self.request(
            MarketStatusRequest(self.authToken))

    def options_list(self, symbol, **kwargs):
        """
        Given the provided underlying symbol, get a list of available options.
        You may optionally include the following boolean flags for more info:

        quarterlies: include quarterly options
        weeklies: include weekly options
        """

        return self.request(
            ViewSeriesRequest(self.authToken, symbol, **kwargs))

    def preview_order(self, account, order):
        """
        Given an account and an Order object, preview details about the order
        and the effect it will have on your account
        """

        return self.request(
            AccountMarginJsonRequest(self.authToken, account, order))

    def place_order(self, account, order):
        """
        Given an account and an Order object, actually place the order
        """

        return self.request(
            OrderCreateJsonRequest(self.authToken, account, order))

    def modify_order(self, account, order, old_order_id):
        """
        For the given account, ask optionshouse to replace an existing order
        with a new one. The exisitng order must be specified using the
        old_order_id argument.
        """

        order.modify(old_order_id)

        return self.request(
            OrderModifyJsonRequest(self.authToken, account, order))

    def cancel_order(self, account, order_id):
        """
        Given an account and an order_id, ask optionshouse to cancel the order
        """

        return self.request(
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

        return self.request(
            MasterAccountOrdersRequest(self.authToken, account, **kwargs))

    def account_positions(self, account):
        """
        Query all the positions held by the given account including current
        price and cost basis information
        """

        try:
            response = self.request(
                AccountPositionsRequest(self.authToken, account))
        except OhRequestException as e:
            if "positions" in e.errors:
                if e.errors["positions"] == "none found":
                    # This is a stupid error because no positions is a
                    # perfectly normal condition, we'll just return an empty
                    # array like optionshouse should

                    return {"unified": []}

            else:
                # Something else went wrong, so re-raise
                raise e

        return response

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

        return self.request(
            AccountActivityRequest(self.authToken, account, **kwargs))

    def request(self, ohreq):
        """
        Actually take a naked request object and send it to optionshouse.
        Instead of calling this directly, you should call one of the session
        helper methods.
        """

        now = time.time()
        sleep_time = 0

        if self.last_request_time != None:
            delta = now - self.last_request_time

            if delta < self.TIME_BETWEEN_REQUESTS:
                sleep_time = self.TIME_BETWEEN_REQUESTS - delta
                self.wait(sleep_time)

        self.last_request_time = now + sleep_time

        return self.issue_request(ohreq)

    def issue_request(self, ohreq):
        try:
            oh_res = urlopen(ohreq.request())
        except HTTPError as e:
            raise OhConnectionException('HTTP code: ', e.code)
        except URLError as e:
            raise OhConnectionException(
                'Server could not be reached: ', e.reason)
        else:
            return self.parse_response(oh_res)

    def parse_response(self, ohres):
        response = json.loads(ohres.read())['EZMessage']

        if 'errors' in response:
            raise OhRequestException(response['errors'])
        elif 'data' in response:
            return response['data']

