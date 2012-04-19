from request import *
import unittest

class TestLoginRequest(unittest.TestCase):

    def test_proper_login_request(self):
        req = LoginRequest('abc', '123')

        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
        self.assertEqual(req.action, 'auth.login')

        expected_data = {
            'userName': 'abc',
            'password': '123',
        }
        self.assertEqual(req.data, expected_data)
        self.assertEqual(req.body(), 'r=' + json.dumps({
            'EZMessage': {
                'action': 'auth.login',
                'data': expected_data,
            }
        }))

class TestLogoutRequest(unittest.TestCase):

    def test_proper_logout_request(self):
        req = LogoutRequest('989_some_session_token_878')

        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
        self.assertEqual(req.action, 'auth.logout')

        expected_data = {
            'authToken': '989_some_session_token_878',
        }
        self.assertEqual(req.data, expected_data)
        self.assertEqual(req.body(), 'r=' + json.dumps({
            'EZMessage': {
                'action': 'auth.logout',
                'data': expected_data,
            }
        }))

class TestAccountInfoRequest(unittest.TestCase):

    def test_proper_account_info_request(self):
        req = AccountInfoRequest('989_some_session_token_878')

        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
        self.assertEqual(req.action, 'account.info')

        expected_data = {
            'authToken': '989_some_session_token_878',
        }
        self.assertEqual(req.data, expected_data)
        self.assertEqual(req.body(), 'r=' + json.dumps({
            'EZMessage': {
                'action': 'account.info',
                'data': expected_data,
            }
        }))


class TestAccountCashRequest(unittest.TestCase):

    def test_proper_account_cash_request(self):
        authToken = '83982734324_someauthtoken'
        account = '324234_someaccount'
        possible_flags = [
            {},
            { 'portfolio': True },
            { 'historical': True },
            { 'fastValues': True },
            { 'portfolio': True, 'historical': True },
            { 'portfolio': False, 'historical': True, 'fastValues': True },
            { 'garbage': True, 'historical': True },
        ]

        for flags in possible_flags:
            req = AccountCashRequest(authToken, account, **flags)

            expected_data = {
                'authToken': authToken,
                'account': account,
            }

            if 'portfolio' in flags and flags['portfolio']:
                expected_data['portfolio'] = True
            if 'historical' in flags and flags['historical']:
                expected_data['historical'] = True
            if 'fastValues' in flags and flags['fastValues']:
                expected_data['fastValues'] = True

            self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
            self.assertEqual(req.action, 'account.cash')
            self.assertEqual(req.data, expected_data)
            self.assertEqual(req.body(), 'r=' + json.dumps({
                'EZMessage': {
                    'action': 'account.cash',
                    'data': expected_data,
                }
            }))


class TestKeepAliveRequest(unittest.TestCase):

    def test_keep_alive_request(self):
        authToken = '83982734358_someauthtoken'
        account = '32419_someaccount'
        req = KeepAliveRequest(authToken, account)

        expected_data = {
            'authToken': authToken,
            'account': account,
        }

        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
        self.assertEqual(req.action, 'auth.keepAlive')
        self.assertEqual(req.data, expected_data)
        self.assertEqual(req.body(), 'r=' + json.dumps({
            'EZMessage': {
                'action': 'auth.keepAlive',
                'data': expected_data,
            }
        }))


class TestViewQuoteListRequest(unittest.TestCase):

    def test_view_quote_list_request(self):
        authToken = '83982734324_someauthtoken'
        key = [ 'COP:::S' ]
        possible_flags = [
            {},
            { 'extended': True },
            { 'stock_details': True },
            { 'fundamental_details': True },
            { 'extended': True, 'stock_details': True },
            { 'extended': False, 'fundamental_details': True },
            { 'garbage': True, 'stock_details': True },
        ]

        for flags in possible_flags:
            req = ViewQuoteListRequest(authToken, key, **flags)

            expected_data = {
                'authToken': authToken,
                'key': key,
            }

            if 'extended' in flags and flags['extended']:
                expected_data['addExtended'] = key
            if 'stock_details' in flags and flags['stock_details']:
                expected_data['addStockDetails'] = key
            if 'fundamental_details' in flags and flags['fundamental_details']:
                expected_data['addFundamentalDetails'] = key

            self.assertEqual(req.endpoint, 'https://api.optionshouse.com/j')
            self.assertEqual(req.action, 'view.quote.list')
            self.assertEqual(req.data, expected_data)
            self.assertEqual(req.body(), 'r=' + json.dumps({
                'EZMessage': {
                    'action': 'view.quote.list',
                    'data': expected_data,
                }
            }))


class TestViewSeriesRequest(unittest.TestCase):

    def test_view_series_request(self):
        authToken = '83982734358_someauthtoken'
        possible_flags = [
            {},
            { 'quarterlies': True },
            { 'weeklies': True },
            { 'quarterlies': True, 'weeklies': True },
            { 'quarterlies': False, 'weeklies': True },
            { 'garbage': True, 'stock_details': True },
        ]

        for flags in possible_flags:
            expected_data = {
                'authToken': authToken,
                'symbol': 'T:::S',
            }

            if 'quarterlies' in flags and flags['quarterlies']:
                expected_data['quarterlies'] = True
            if 'weeklies' in flags and flags['weeklies']:
                expected_data['weeklies'] = True

            req = ViewSeriesRequest(authToken, 'T:::S', **flags)
            self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
            self.assertEqual(req.action, 'view.series')
            self.assertEqual(req.data, expected_data)
            self.assertEqual(req.body(), 'r=' + json.dumps({
                'EZMessage': {
                    'action': 'view.series',
                    'data': expected_data,
                }
            }))


class TestAccountMarginJsonRequest(unittest.TestCase):
    def test_proper_amj_request(self):
        class FakeOrder:
            def toDict(self):
                return { 'order': 'withthefakeness' }

        authToken = '83982734358_someauthtoken'
        account = '32419_someaccount'
        order = FakeOrder()
        expected_data = {
            'authToken': authToken,
            'account': account,
            'order': order.toDict(),
        }

        req = AccountMarginJsonRequest(authToken, account, order)
        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/j')
        self.assertEqual(req.action, 'account.margin.json')
        self.assertEqual(req.data, expected_data)


if __name__ == '__main__':
    unittest.main()
