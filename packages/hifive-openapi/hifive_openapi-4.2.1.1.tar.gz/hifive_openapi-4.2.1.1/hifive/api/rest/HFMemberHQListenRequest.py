from hifive.api.base import RestApi

class HFMemberHQListenRequest(RestApi):
    def __init__(self, domain=None, port=80, method=None):
        domain = domain or 'hifive-gateway-test.hifiveai.com';
        method = method or 'GET';
        RestApi.__init__(self,domain, port ,method)
        self.accessToken = None
        self.musicId = None
        self.audioFormat = None
        self.audioRate = None


    def getapiname(self):
        return 'MemberHQListen'