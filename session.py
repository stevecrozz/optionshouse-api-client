import urllib2
import json
from request import LoginRequest, KeepAliveRequest, LogoutRequest

class Session(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.state = 'closed'
        self.authToken = None

    def open(self):
        oh_res = self.issue_request(
            LoginRequest(self.username, self.password)
        )

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
            LogoutRequest(self.authToken)
        )

        if 'logout' in oh_res:
            self.authToken = None
            self.state = 'closed'
        else:
            print oh_res

    def keepalive(self, account):
        oh_res = self.issue_request(
            KeepAliveRequest(self.authToken, account)
        )

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

