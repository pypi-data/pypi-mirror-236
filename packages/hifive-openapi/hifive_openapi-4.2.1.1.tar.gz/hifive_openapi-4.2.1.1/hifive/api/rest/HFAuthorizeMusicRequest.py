'''
Created by yong.huang on 2016.11.04
'''
from hifive.api.base import RestApi
class HFAuthorizeMusicRequest(RestApi):
	def __init__(self, domain=None, port=80, method=None):
		domain = domain or 'hifive-gateway-test.hifiveai.com'
		method = method or 'POST'
		RestApi.__init__(self, domain, port, method)
		self.clientId = None
		self.Page = None
		self.PageSize = None
		self.subVersion = None
		self.authStartTime = None
		self.authEndTime = None
		self.musicId = None
		self.authArea = None
		self.taskId = None



	def getapiname(self):
		return 'AuthorizeMusic'
