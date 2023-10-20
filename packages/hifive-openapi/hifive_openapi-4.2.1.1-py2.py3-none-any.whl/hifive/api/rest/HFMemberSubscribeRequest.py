from hifive.api.base import RestApi

class HFMemberSubscribeRequest(RestApi):
    def __init__(self, domain=None, port=80, method=None):
        domain = domain or 'hifive-gateway-test.hifiveai.com';
        method = method or 'POST';
        RestApi.__init__(self,domain, port ,method)
        self.accessToken = None
        self.orderId = None
        self.memberPriceId = None
        self.totalFee = None
        self.startTime = None
        self.endTime = None
        self.remark = None


    def getapiname(self):
        return 'MemberSubscribe'