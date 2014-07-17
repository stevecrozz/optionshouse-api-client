import sys
if 'optionshouse' not in sys.path:
    sys.path.append('optionshouse')

import mock, unittest, inspect, request

class TestSession(unittest.TestCase):

    AUTH_TOKEN = 'AuThTOkEN!'
    ACCOUNT = 'AKOWNT123'
    KWARGS = {
        'a': 'b',
        'c': 'delicious',
    }
    ORDER = '<<<ORDER>>>'

    @classmethod
    def setUpClass(cls):
        cls.request_mocks = []

        for i in inspect.getmembers(request, inspect.isclass):
            """
            Mock all the request objects. We only need to make sure they're
            being instantiated correctly. Request testing is done separately.
            """

            request_mock = mock.patch("request.%s" % i[0])
            request_mock.start()
            cls.request_mocks.append(request_mock)

    @classmethod
    def tearDownClass(cls):
        mock.patch.stopall()

    def get_open_session(self):
        import session
        s = session.Session('mike', 'mikepassword')
        s.authToken = self.AUTH_TOKEN
        return s

    def test_bare_session(self):
        import session
        s = session.Session('joe', 'joespassword')
        self.assertEqual(s.state, 'closed')
        self.assertEqual(s.authToken, None)

    def test_session_open(self):
        import session
        issue_req_mock = mock.patch('session.Session.issue_request',
            return_value={ 'authToken': 'someauthtoken!!' })
        issue_req_mock.start()

        s = session.Session('joe', 'joespassword')
        s.open()
        request.LoginRequest.assert_called_with('joe', 'joespassword')
        self.assertEqual(s.authToken, 'someauthtoken!!')
        self.assertEqual(s.state, 'open')
        issue_req_mock.stop()

    def test_session_close(self):
        issue_req_mock = mock.patch('session.Session.issue_request',
            return_value={ 'logout' : 'whatever' })
        issue_req_mock.start()

        self.get_open_session().close()

        request.LogoutRequest.assert_called_with(self.AUTH_TOKEN)
        issue_req_mock.stop()

    def test_keepalive(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().keepalive(self.ACCOUNT)

        request.KeepAliveRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT)
        issue_req_mock.stop()

    def test_account_info(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().account_info()

        request.AccountInfoRequest.assert_called_with(self.AUTH_TOKEN)
        issue_req_mock.stop()

    def test_account_cash(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().account_cash(self.ACCOUNT)
        request.AccountCashRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT)

        self.get_open_session().account_cash(self.ACCOUNT, **self.KWARGS)
        request.AccountCashRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT, **self.KWARGS)

        issue_req_mock.stop()

    def test_market_status(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().market_status()
        request.MarketStatusRequest.assert_called_with(self.AUTH_TOKEN)

    def test_quote(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().quote(['F:::S'])
        request.ViewQuoteListRequest.assert_called_with(self.AUTH_TOKEN,
            ['F:::S'])

        self.get_open_session().quote(['F:::S'], **self.KWARGS)
        request.ViewQuoteListRequest.assert_called_with(self.AUTH_TOKEN,
            ['F:::S'], **self.KWARGS)

        issue_req_mock.stop()

    def test_options_list(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().options_list('F')
        request.ViewSeriesRequest.assert_called_with(self.AUTH_TOKEN, 'F')

        self.get_open_session().options_list('F', **self.KWARGS)
        request.ViewSeriesRequest.assert_called_with(self.AUTH_TOKEN, 'F',
            **self.KWARGS)

        issue_req_mock.stop()

    def test_preview_order(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().preview_order(self.ACCOUNT, self.ORDER)
        request.AccountMarginJsonRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT, self.ORDER)

        issue_req_mock.stop()

    def test_place_order(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().place_order(self.ACCOUNT, self.ORDER)
        request.OrderCreateJsonRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT, self.ORDER)

        issue_req_mock.stop()

    def test_cancel_order(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().cancel_order(self.ACCOUNT, 99)
        request.OrderCancelJsonRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT, 99)

        issue_req_mock.stop()

    def test_list_orders(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().list_orders(self.ACCOUNT)
        request.MasterAccountOrdersRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT)

        self.get_open_session().list_orders(self.ACCOUNT, **self.KWARGS)
        request.MasterAccountOrdersRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT, **self.KWARGS)

        issue_req_mock.stop()

    def test_account_positions(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().account_positions(self.ACCOUNT)
        request.AccountPositionsRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT)

        issue_req_mock.stop()

    def test_account_activity(self):
        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()

        self.get_open_session().account_activity(self.ACCOUNT)
        request.AccountActivityRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT)

        self.get_open_session().account_activity(self.ACCOUNT, **self.KWARGS)
        request.AccountActivityRequest.assert_called_with(self.AUTH_TOKEN,
            self.ACCOUNT, **self.KWARGS)

        issue_req_mock.stop()

    def test_rate_limit(self):
        """
        Make sure we're helpfully rate-limiting requests to optionshouse. We
        should be good and try to avoid clients accidently DoSing optionshouse.
        """

        issue_req_mock = mock.patch('session.Session.issue_request')
        issue_req_mock.start()
        mock_wait = mock.patch('session.Session.wait')
        mock_wait.start()

        mock_time = mock.patch("time.time", return_value=1.0)
        mock_time.start()
        s = self.get_open_session()
        s.account_activity(self.ACCOUNT)
        mock_time.stop()
        self.assertEqual(s.last_request_time, 1.0)

        mock_time = mock.patch("time.time", return_value=1.5)
        mock_time.start()
        s.keepalive(self.ACCOUNT)
        mock_time.stop()
        s.wait.assert_called_once_with(0.5)
        self.assertEqual(s.last_request_time, 2.0)

        mock_time = mock.patch("time.time", return_value=4.5)
        mock_time.start()

        # This will raise an exception if the session tries to call #wait
        s.wait = "can't call a string"
        s.keepalive(self.ACCOUNT)
        mock_time.stop()

        issue_req_mock.stop()
        mock_wait.stop()



if __name__ == '__main__':
    unittest.main()
