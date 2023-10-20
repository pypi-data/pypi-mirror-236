from hifive.api.base import RestApi

class HFMemberSubscribePayRequest(RestApi):
    def __init__(self, domain=None, port=80, method=None):
        domain = domain or 'hifive-gateway-test.hifiveai.com';
        method = method or 'POST';
        RestApi.__init__(self,domain, port ,method)
        self.accessToken = None
        self.orderId = None
        self.memberPriceId = None
        self.totalFee = None
        self.payType = None
        self.qrCodeSize = None
        self.callbackUrl = None
        self.remark = None


    def getapiname(self):
        return 'MemberSubscribePay'