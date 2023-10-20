from hifive.api.base import RestApi

class HFMemberPriceRequest(RestApi):
    def __init__(self, domain=None, port=80, method=None):
        domain = domain or 'hifive-gateway-test.hifiveai.com';
        method = method or 'GET';
        RestApi.__init__(self,domain, port ,method)
        self.accessToken = None


    def getapiname(self):
        return 'MemberPrice'