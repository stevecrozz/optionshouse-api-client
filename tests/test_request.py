import sys
if 'optionshouse' not in sys.path:
    sys.path.append('optionshouse')

from request import *
import unittest

if sys.version_info[0] < 3:
    from urlparse import parse_qs
else:
    from urllib.parse import parse_qs

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

        parsed_body = json.loads(parse_qs(req.body())['r'][0])
        self.assertEqual(parsed_body, {
            'EZMessage': {
                'action': 'auth.login',
                'data': expected_data,
            }
        })

class TestLogoutRequest(unittest.TestCase):

    def test_proper_logout_request(self):
        req = LogoutRequest('989_some_session_token_878')

        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
        self.assertEqual(req.action, 'auth.logout')

        expected_data = {
            'authToken': '989_some_session_token_878',
        }
        self.assertEqual(req.data, expected_data)
        parsed_body = json.loads(parse_qs(req.body())['r'][0])
        self.assertEqual(parsed_body, {
            'EZMessage': {
                'action': 'auth.logout',
                'data': expected_data,
            }
        })

class TestAccountInfoRequest(unittest.TestCase):

    def test_proper_account_info_request(self):
        req = AccountInfoRequest('989_some_session_token_878')

        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
        self.assertEqual(req.action, 'account.info')

        expected_data = {
            'authToken': '989_some_session_token_878',
        }
        self.assertEqual(req.data, expected_data)
        parsed_body = json.loads(parse_qs(req.body())['r'][0])
        self.assertEqual(parsed_body, {
            'EZMessage': {
                'action': 'account.info',
                'data': expected_data,
            }
        })

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
            parsed_body = json.loads(parse_qs(req.body())['r'][0])
            self.assertEqual(parsed_body, {
                'EZMessage': {
                    'action': 'account.cash',
                    'data': expected_data,
                }
            })

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
        parsed_body = json.loads(parse_qs(req.body())['r'][0])
        self.assertEqual(parsed_body, {
            'EZMessage': {
                'action': 'auth.keepAlive',
                'data': expected_data,
            }
        })

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
            parsed_body = json.loads(parse_qs(req.body())['r'][0])
            self.assertEqual(parsed_body, {
                'EZMessage': {
                    'action': 'view.quote.list',
                    'data': expected_data,
                }
            })

class TestMarketStatusRequest(unittest.TestCase):

    def test_market_status_request(self):
        authToken = '83982734324_someauthtoken'
        req = MarketStatusRequest(authToken)
        expected_data = {
            'authToken': authToken,
            'key': ['MARKETSTATUS'],
        }

        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
        self.assertEqual(req.action, 'view.quote.list')
        self.assertEqual(req.data, expected_data)
        parsed_body = json.loads(parse_qs(req.body())['r'][0])
        self.assertEqual(parsed_body, {
            'EZMessage': {
                'action': 'view.quote.list',
                'data': expected_data,
            }
        })

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
            parsed_body = json.loads(parse_qs(req.body())['r'][0])
            self.assertEqual(parsed_body, {
                'EZMessage': {
                    'action': 'view.series',
                    'data': expected_data,
                }
            })

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
        parsed_body = json.loads(parse_qs(req.body())['r'][0])
        self.assertEqual(parsed_body, {
            'EZMessage': {
                'action': 'account.margin.json',
                'data': expected_data,
            }
        })

class TestOrderCreateJsonRequest(unittest.TestCase):
    def test_proper_order_create_request(self):
        class FakeOrder:
            def toDict(self):
                return { 'order': 'withthefakeness!!' }

        authToken = '83982734331_someauthtoken'
        account = '32404_someaccount'
        order = FakeOrder()
        expected_data = {
            'authToken': authToken,
            'account': account,
            'order': order.toDict(),
        }

        req = OrderCreateJsonRequest(authToken, account, order)
        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/j')
        self.assertEqual(req.action, 'order.create.json')
        self.assertEqual(req.data, expected_data)
        parsed_body = json.loads(parse_qs(req.body())['r'][0])
        self.assertEqual(parsed_body, {
            'EZMessage': {
                'action': 'order.create.json',
                'data': expected_data,
            }
        })

class TestOrderModifyJsonRequest(unittest.TestCase):
    def test_proper_order_modify_request(self):
        class FakeOrder:
            def toDict(self):
                return { 'order': 'fakecancelorder' }

        authToken = '83982734331_someauthtoken'
        account = '32404_someaccount'
        order = FakeOrder()
        expected_data = {
            'authToken': authToken,
            'account': account,
            'order': order.toDict(),
        }

        req = OrderModifyJsonRequest(authToken, account, order)
        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/j')
        self.assertEqual(req.action, 'order.modify.json')
        self.assertEqual(req.data, expected_data)
        parsed_body = json.loads(parse_qs(req.body())['r'][0])
        self.assertEqual(parsed_body, {
            'EZMessage': {
                'action': 'order.modify.json',
                'data': expected_data,
            }
        })

class TestOrderCancelJsonRequest(unittest.TestCase):
    def test_proper_order_cancel_request(self):
        authToken = '83982734331_someauthtoken'
        account = '32404_someaccount'
        expected_data = {
            'authToken': authToken,
            'account': account,
            'order_id': 888222,
        }

        req = OrderCancelJsonRequest(authToken, account, 888222)
        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/j')
        self.assertEqual(req.action, 'order.cancel.json')
        self.assertEqual(req.data, expected_data)
        parsed_body = json.loads(parse_qs(req.body())['r'][0])
        self.assertEqual(parsed_body, {
            'EZMessage': {
                'action': 'order.cancel.json',
                'data': expected_data,
            }
        })

class TestMasterAccountOrdersRequest(unittest.TestCase):
    def test_proper_request(self):
        authToken = '83982734331_someauthtoken'
        account = '32404_someaccount'

        possible_flags = [
            { },
            { 'archived': True, 'page': 9 },
            { 'symbol': 'SSO' },
            { 'page': 2 },
            { 'page_count': 5 },
            { 'page': 3, 'page_count': 20, 'page_size': 100 },
            { 'garbage': True, 'symbol': 'CSCO' },
        ]

        for flags in possible_flags:
            req = MasterAccountOrdersRequest(authToken, account, **flags)

            # Note the 'account_id' parameter which is different from all the
            # other requests which require an 'account' parameter
            expected = {
                'authToken': authToken,
                'account_id': account,
                'master_order': {
                    'master_order_view': 'current',
                },
            }

            if 'symbol' in flags:
                expected['symbol'] = flags['symbol']
            if 'page' in flags:
                expected['master_order']['page'] = flags['page']
            if 'page_count' in flags:
                expected['master_order']['page_count'] = flags['page_count']
            if 'page_size' in flags:
                expected['master_order']['page_size'] = flags['page_size']
            if 'archived' in flags and flags['archived'] == True:
                expected['master_order']['master_order_view'] = 'archived'

            self.assertEqual(req.endpoint, 'https://api.optionshouse.com/j')
            self.assertEqual(req.action, 'master.account.orders')
            self.assertEqual(req.data, expected)
            parsed_body = json.loads(parse_qs(req.body())['r'][0])
            self.assertEqual(parsed_body, {
                'EZMessage': {
                    'action': 'master.account.orders',
                    'data': expected,
                }
            })

class TestAccountPositionsRequest(unittest.TestCase):
    def test_account_positions_request(self):
        authToken = '83982734331_someauthtoken'
        account = '32404_someaccount'
        expected_data = {
            'authToken': authToken,
            'account': account,
        }

        req = AccountPositionsRequest(authToken, account)
        self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
        self.assertEqual(req.action, 'account.positions')
        self.assertEqual(req.data, expected_data)
        parsed_body = json.loads(parse_qs(req.body())['r'][0])
        self.assertEqual(parsed_body, {
            'EZMessage': {
                'action': 'account.positions',
                'data': expected_data,
            }
        })

class TestAccountActivityRequest(unittest.TestCase):
    def test_account_activity_request(self):
        authToken = '83982734331_someauthtoken'
        account = '32404_someaccount'
        possible_flags = [
            { },
            { 'maxPage': 15, 'page': 9 },
            { 'size': 20 },
            { 'page': 2 },
            { 'totalCount': 5 },
            { 'page': 3, 'totalCount': 20, 'sDate': '01/01/2012' },
            { 'sDate': '03/01/2012', 'eDate': '03/31/2012' },
            { 'symbol': 'GS' },
            { 'garbage': True, 'size': 20 },
        ]

        for flags in possible_flags:
            expected_data = {
                'authToken': authToken,
                'account': account,
            }

            if 'page' in flags:
                expected_data['page'] = flags['page']
            if 'maxPage' in flags:
                expected_data['maxPage'] = flags['maxPage']
            if 'size' in flags:
                expected_data['size'] = flags['size']
            if 'totalCount' in flags:
                expected_data['totalCount'] = flags['totalCount']
            if 'sDate' in flags:
                expected_data['sDate'] = flags['sDate']
            if 'eDate' in flags:
                expected_data['eDate'] = flags['eDate']
            if 'symbol' in flags:
                expected_data['symbol'] = flags['symbol']

            req = AccountActivityRequest(authToken, account, **flags)
            self.assertEqual(req.endpoint, 'https://api.optionshouse.com/m')
            self.assertEqual(req.action, 'account.activity')
            self.assertEqual(req.data, expected_data)
            parsed_body = json.loads(parse_qs(req.body())['r'][0])
            self.assertEqual(parsed_body, {
                'EZMessage': {
                    'action': 'account.activity',
                    'data': expected_data,
                }
            })

if __name__ == '__main__':
    unittest.main()
