#-*- coding: utf-8 -*-
import requests
import time

class YIMA:
	'''
		login yima platform
	'''
	def __init__(self, itemid='2674'):
		'''
			args:
				itemd (2730, 2674)
		'''
		self.url='http://api.51ym.me/UserInterface.aspx'
		self.token = ""
		self.itemid = itemid
		self.mobile = ""
		self.headers = {
			"Content-Type":"text/plain;charset:utf8;"
		}
		
	def login_yima(self):
		'''
			login
		'''
		body={
			'action':'login',
			'username':'gc12306',
			'password':'gaochong1513'
		}
		r=requests.get(self.url,params=body, headers=self.headers)#, headers=self.headers
		result=r.text.split('|')
		token=result[1]
		self.token = token
		#return token


	def get_mobile(self):
		'''
			get mobile for itemd = self.itemid
		'''		
		
		body={
			'action':'getmobile',
			'token':self.token,
			'itemid':self.itemid
		}
		r = requests.get(self.url, params=body)
		result=r.text.split('|')
		if result[0]=='success':
			mobile=result[1]
			self.mobile = mobile
			return mobile
		else:
			return ""
			
	def release_all(self):
		'''
			realease all mobiles
		'''
		body={
			'action':'releaseall',
			'token':self.token
		}
		r = requests.get(self.url, params=body)
		print(r.text)
	
	def get_message(self):
		'''
			get message code
			return:
				message
		'''
		print ("get message.")
		body={
			'action':'getsms',
			'mobile':self.mobile,
			'itemid':self.itemid,
			'token':self.token
		}
		sms="3001"
		while sms=='3001':
			r = requests.get(self.url, params=body)
			sms = r.content.decode("utf-8")
			print ("message:%s"%sms)
			time.sleep(5)
		sms=sms.split('|')[1]
		return sms
		
	def get_code(self):
		sms = self.get_message()
		print (str(sms))
		if self.itemid == "2730":
			begin = sms.find(':')+1
			end = sms.find(',')
			code=sms[begin:end]
			return code
		elif self.itemid == "2674":
			index = sms.find("。")
			#print("index:{}".format(index))
			return sms[index-4:index]

			
def monkey_patch():
	prop = requests.models.Response.content
	def content(self):
		_content = prop.fget(self)
		if self.encoding == 'ISO-8859-1':
			encodings = requests.utils.get_encodings_from_content(_content)
			if encodings:
				self.encoding = encodings[0]
			else:
				self.encoding = self.apparent_encoding
			_content = _content.decode(self.encoding, 'replace').encode('utf8', 'replace')
			self._content = _content
		return _content
	requests.models.Response.content = property(content)

			
def test_sms():
		sms = "【趣头条】您的验证码是6281。如非本人操作，请忽略本短信"
		sms.encode("utf8").decode("ISO-8859-1")
		print(sms)
		index = sms.find("。")
		print(sms[index-4:index])
		
def main():
	ym = YIMA()
	ym.login_yima()
	print(ym.token)
	ym.get_mobile()
	print(ym.mobile)
	ym.release_all()
		
if "__main__" == __name__:
	#test_sms()
	main()
	#monkey_patch()
