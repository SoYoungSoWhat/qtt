#-*- coding: utf-8 -*-

import requests
import hashlib
import random
import time
import uuid
import json
import threading
import base64
import pytesseract
from PIL import Image, ImageDraw
import os
from sys import argv
from yima import YIMA
from userinfo import UserInfoService

uis = UserInfoService()
lock = threading.Lock()

class JZ(object):
	'''
		process a picture
	'''
	def __init__(self, input, G=100):
		'''
			init
			args:
				input: image path
				G: the threshold of RGB
		'''
		self.image = Image.open(input)
		self.G = G
		#self.output = output
	
	def get_near_point_num(self, x, y):
		'''
			get near point number
			args:
				x,y: point
			return:
				the number of near (x,y)
		'''
		nearDots = 0
		if (self.image.getpixel((x - 1,y - 1))[0] > self.G):
			nearDots += 1
		if (self.image.getpixel((x - 1,y))[0] > self.G):
			nearDots += 1
		if (self.image.getpixel((x - 1,y + 1))[0] > self.G):
			nearDots += 1
		if (self.image.getpixel((x,y - 1))[0] > self.G):
			nearDots += 1
		if (self.image.getpixel((x,y + 1))[0] > self.G):
			nearDots += 1
		if (self.image.getpixel((x + 1,y - 1))[0] > self.G):
			nearDots += 1
		if (self.image.getpixel((x + 1,y))[0] > self.G):
			nearDots += 1
		if (self.image.getpixel((x + 1,y + 1))[0] > self.G):
			nearDots += 1
		return nearDots
		
	def clear_like_white(self):
		'''
			clear like white pixel
		'''
		draw = ImageDraw.Draw(self.image)
		WHITH_COLOR = (255,255,255)
		for x in range(1, self.image.size[0] - 1):
			for y in range(1, self.image.size[1] - 1):
				color = self.image.getpixel((x, y))
				if color[0]>self.G:
					draw.point((x,y),WHITH_COLOR)

	
	def clear_solid_point(self):
		'''
			clear solid point
		'''
		draw = ImageDraw.Draw(self.image)
		WHITH_COLOR = (255,255,255)
		N_T = 6 #the threshold of near
		for x in range(1, self.image.size[0] - 1):
			for y in range(1, self.image.size[1] - 1):
				nearDots = self.get_near_point_num(x, y)
				if nearDots > N_T:
					draw.point((x,y),WHITH_COLOR)
					
	def clear_frame(self):
		'''
			clear up down left right 
			one pixel
		'''
		draw = ImageDraw.Draw(self.image)
		w, h = self.image.size
		WHITH_COLOR = (255,255,255)
		for x in range(0, w):
			draw.point((x, 0), WHITH_COLOR)
			draw.point((x, h-1), WHITH_COLOR)
			
		for y in range(0, h):
			draw.point((0, y), WHITH_COLOR)
			draw.point((w-1, y), WHITH_COLOR)

	def get_code(self):
		'''
			run
		'''
		#1. clear like white point
		self.clear_like_white()
		#2. clear sloid point
		self.clear_solid_point()
		#3. clear frame
		self.clear_frame()
		#4. get code 
		code = pytesseract.image_to_string(self.image)
		res_code = ""
		if len(code) >= 4:
			for i in range(len(code)):
				char_i = code[i]
				if char_i.isdigit():
					res_code += char_i
			if len(res_code) == 4:
				return res_code
			else:
				return None
		else:
			return None
		
			
class QTT(object):

	'''
		class QTT
		
	'''

	def __init__(self, telephone, device_code, password="123456"):
		'''
			init some values
		'''
		self.telephone = telephone
		self.password = str(password)
		self.token = ""
		self.device_code = device_code
		self.uuid1 = str(uuid.uuid1())
		self.member_info = {}
		self.lat = str(self.get_lat())
		self.lon = str(self.get_lon())
		#print("lat:{}, type:{}".format(self.lat, type(self.lat)))
		
		self.channel_list = [{'id': 255, 'name': '推荐'}, {'id': 1, 'name': '热点'}, {'id': 6, 'name': '娱乐'}, {'id': 5, 'name': '养生'}, {'id': 2, 'name': '搞笑'}, {'id': 3, 'name': '奇闻'}, {'id': 4, 'name': '励志'}, {'id': 7, 'name': '科技'}, {'id': 8, 'name': '生活'}, {'id': 10, 'name': '财经'}, {'id': 9, 'name': '汽车'}, {'id': 11, 'name': '情感'}, {'id': 18, 'name': '星座'}, {'id': 12, 'name': '美食'}, {'id': 14, 'name': '时尚'}, {'id': 16, 'name': '旅游'}, {'id': 17, 'name': '育儿'}, {'id': 13, 'name': '体育'}, {'id': 15, 'name': '军事'}, {'id': 23, 'name': '历史'}, {'id': 27, 'name': '三农'}]
	
	def read_list(self, read_count):
		'''
			complete reading task
			args:
				read_count: read count
		'''
		total_read = 0
		flag = True
		MAX_SIZE = len(self.channel_list)
		while flag and total_read < read_count:
			cid = random.randint(0, MAX_SIZE-1)
			cid = self.channel_list[cid]['id']
			#1. get content list
			#print("get content list")
			content_list = self.get_content_list(cid)
			#print(content_list)
			
			for index,content in enumerate(content_list):
				time.sleep(2)
				#print(content)
				if "id" in content:
					content_id = content["id"]
				else:
					continue
				#print("content_id: {}".format(content_id))
				#2. get content 
				data = self.get_content(content_id)
				key = self.get_key(data)
				time.sleep(3)
				#3. get content view
				self.get_content_view(key)
				#4. get content read
				time.sleep(random.randint(5, 8))
				if index % 2 == 0:
					result = self.get_content_read(key)
					amount = self.get_read_amount(result)
					print("get amount:{} total_read: {}".format(amount, total_read+1))
					if amount > 0:
						total_read += 1
						if total_read >= read_count:
							break
					else:
						flag = False
						break
		return total_read
	'''
	##########################################
	#	util methods
	##########################################
	'''
	
	def parse_url(self, url):
		'''
			parse url
			args:
				url: url?p1=v1&p2=v2
			return:
				params dict({p1:v1, ...})
		'''
		two_part = url.split("?")
		uri = two_part[0]
		params = two_part[1]
		param_list = params.split("&")
		params_dic = {}
		for param in param_list:
			two_part = param.split("=")
			params_dic[two_part[0]] = two_part[1]
		return params_dic
	def get_lat(self):
		lat=40.41336
		r = round(random.random()*random.randint(1,3), 4)
		s = random.randint(1, 100)
		if s%2 == 0:
			return lat + r
		else:
			return lat - r 
	def get_lon(self):
		lon=116.671
		r = round(random.random()*random.randint(1,4), 4)
		s = random.randint(1, 100)
		if s%2 == 0:
			return lon + r
		else:
			return lon - r 
	
	def get_key(self, data):
		'''
			get key
			args:data [{:, "key":"value",...}]
		'''
		data = data[0]
		url = data['url']
		params = self.parse_url(url)
		key = params['key']
		return key
		
	def get_sign(self, params):
		'''
			get only sign
		'''
		key = "&key=txscP6NCs3U6AIgT"
		params += key
		m = hashlib.md5()
		m.update(params.encode())
		return m.hexdigest()
		
	def get_read_amount(self, result):
		'''
			get the amount
			args:
				reuslt:Zepto1489901565126({"code":0,"message":"成功","currentTime":1489910517,"data":{"amount":10,"status_code":0}})
			return:
				the amount
		'''
		data = 'Zepto1489901565126({"code":0,"message":"成功","currentTime":1489910517,"data":{"amount":10,"status_code":0}})'
		start = data.find("(")+1
		data = data[start:-1]
		data = json.loads(data)
		amount = data['data']['amount']
		return int(amount)
		
	'''
	##########################################
	#	model methods
	##########################################
	'''
	def get_app_start(self):
		'''
			start app
		'''
		
		url = "http://api.1sapp.com/app/start?"
		params = "OSVersion=4.4.2&brand=samsung&client_version=20200&device=192567455774068&deviceCode=192567455774068&dtu=004&lat=0.0&lon=0.0&manufacturer=samsung&model=GT-N7100&network=wifi&time=1489804499314&uuid=f65006be091843d1b277bdd11d287fcb&version=20200"
		sign = self.get_sign(params)
		url = url+params+"&sign="+sign
		headers = {
			"User-Agent": "qukan_android",
			"Host": "api.1sapp.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		res = requests.get(url, headers=headers)
		print(res.text)
	
	def get_app_get_config(self):
		'''
			get config
		'''
		url = "http://api.1sapp.com/app/getConfig?"
		params = "OSVersion=4.4.2&deviceCode=192567455774068&dtu=004&lat=40.41336&lon=116.671&network=wifi&time=1489804500234&token=&type=wifi_report&uuid=f65006be091843d1b277bdd11d287fcb&version=20200"
		sign = self.get_sign(params)
		url = url+params+"&sign="+sign
		headers = {
			"User-Agent": "qukan_android",
			"Host": "api.1sapp.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		res = requests.get(url, headers=headers)
		print(res.text)
	
	
	def get_content_channel_list(self):
		'''
			get default channel list
			return:
				data [{"id":5,"name":"养生"},...]
		'''
		url = "http://api.1sapp.com/content/getDefaultChannelList?"
		params = "OSVersion=4.4.2&deviceCode=192567455774068&dtu=004&lat=40.41336&lon=116.671&network=wifi&time=1489804500314&uuid=f65006be091843d1b277bdd11d287fcb&version=20200"
		sign = self.get_sign(params)
		url = url+params+"&sign="+sign
		headers = {
			"User-Agent": "qukan_android",
			"Host": "api.1sapp.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		res = requests.get(url, headers=headers)
		data = json.loads(res.text)
		self.channel_list = data['data']
		return data['data']
	
	def get_member_login(self):
		'''
			login
		'''
		
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/member/login?"
		params = "OSVersion=4.4.2&deviceCode="+self.device_code+"&dtu=001&lat="+self.lat+"&lon="+self.lon+"&network=wifi&password="+self.password+"&telephone="+self.telephone+"&time="+time_now+"&uuid="+self.uuid1+"&version=20200"
		sign = self.get_sign(params)
		url = url+params+"&sign="+sign
		headers = {
			"User-Agent": "qukan_android",
			"Host": "api.1sapp.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		
		res = requests.get(url, headers=headers)
		#print(res.text)
		data = json.loads(res.text)['data']
		self.token = data['token']
		
	def get_member_info(self):
		'''
			get member info
			return:
				member info dict{}
				example:
					{'member_id': '5573044', 'telephone': '15503820160', 'nickname': '趣友5573044', 'birth': '', 'balance': '5.06', 'coin': 32, 'status': '1', 'invite_code': 'A5573044', 'is_bind_wx': 0, 'gift_notice': {}, 'gift_coin_notice': {}, 'loop_pic': [], 'pupil_num': 0, 'teacher_id': '5571430', 'is_fresher': False, 'prov': '北京市', 'city': '北京市'}
		'''
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/member/getMemberInfo?"
		params = "OSVersion=4.4.2&deviceCode="+self.device_code+"&dtu=004&lat="+self.lat+"&lon="+self.lon+"&network=wifi&time="+time_now+"&token="+self.token+"&uuid="+self.uuid1+"&version=20200"
		sign = self.get_sign(params)
		url = url+params+"&sign="+sign
		headers = {
			"User-Agent": "qukan_android",
			"Host": "api.1sapp.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		
		res = requests.get(url, headers=headers)
		data = json.loads(res.text)['data']
		data.pop('menu')
		data.pop('avatar')
		data.pop('h5_url')
		self.member_info = data
		
	def get_app_config(self):
		'''
			get app config
		'''
		
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/app/getConfig?token="+self.token+"&dtu=200&type=h5_config&_="+time_now
		
		headers = {
			"Host": "api.1sapp.com",
			"Connection": "keep-alive",
			"Accept": "application/json",
			"Origin": "http://h5ssl.1sapp.com",
			"User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; GT-N7100 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 qukan_android",
			#Referer": "http://h5ssl.1sapp.com/qukan_new2/dest/old_yq/inapp/old_yq/qd.html?v=20200&lat=40.41336&lon=116.671&network=wifi&dc=192567455774068&dtu=004&uuid=f65006be091843d1b277bdd11d287fcb
			"Accept-Encoding": "gzip,deflate",
			"Accept-Language": "zh-CN,en-US;q=0.8",
			"X-Requested-With": "com.jifen.qukan"
		}
		
		res = requests.get(url, headers=headers)
		print(res.text)

	def get_mission_list(self):
		'''
			get mission list
			return:
				mission list
		'''
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/mission/getMissionList?token="+self.token+"&dtu=200&_="+time_now
		headers = {
			"Host": "api.1sapp.com",
			"Connection": "keep-alive",
			"Accept": "application/json",
			"Origin": "http://h5ssl.1sapp.com",
			"User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; GT-N7100 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 qukan_android",
			"Referer": "http://h5ssl.1sapp.com/qukan_new2/dest/old_yq/inapp/old_yq/qd.html?v=20200&lat=40.41336&lon=116.671&network=wifi&dc="+self.device_code+"&dtu=004&uuid="+self.uuid1,
			"Accept-Encoding": "gzip,deflate",
			"Accept-Language": "zh-CN,en-US;q=0.8",
			"X-Requested-With": "com.jifen.qukan"
		}
		
		res = requests.get(url, headers=headers)
		data = json.loads(res.text)['data']
		return data

	def post_mission_signin(self):
		'''
			sign in
		'''
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/mission/signIn?_="+time_now
		headers = {
			"Host": "api.1sapp.com",
			"Connection": "keep-alive",
			"Accept": "application/json",
			"Origin": "http://h5ssl.1sapp.com",
			"User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; GT-N7100 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 qukan_android",
			"Referer": "http://h5ssl.1sapp.com/qukan_new2/dest/old_yq/inapp/old_yq/qd.html?v=20200&lat=40.41336&lon=116.671&network=wifi&dc="+self.device_code+"&dtu=004&uuid="+self.uuid1,
			"Accept-Encoding": "gzip,deflate",
			"Accept-Language": "zh-CN,en-US;q=0.8",
			"X-Requested-With": "com.jifen.qukan"
		}
		data = {
			"token":self.token,
			'dtu':"200"
		}
		
		res = requests.post(url, headers=headers, data=data)
		print(res.text)
	
	def post_mission_receive_box(self):
		'''
			open a box
		'''
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/mission/receiveTreasureBox?_="+time_now
		headers = {
			"Host": "api.1sapp.com",
			"Connection": "keep-alive",
			"Accept": "application/json",
			"Origin": "http://h5ssl.1sapp.com",
			"User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; GT-N7100 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 qukan_android",
			"Referer": "http://h5ssl.1sapp.com/qukan_new2/dest/old_yq/inapp/old_yq/qd.html?v=20200&lat=40.41336&lon=116.671&network=wifi&dc="+self.device_code+"&dtu=004&uuid="+self.uuid1,
			"Accept-Encoding": "gzip,deflate",
			"Accept-Language": "zh-CN,en-US;q=0.8",
			"X-Requested-With": "com.jifen.qukan"
		}
		data = {
			"token":self.token,
			'dtu':"200"
		}
		
		res = requests.post(url, headers=headers, data=data)
		print(res.text)
		return json.loads(res.text)

	def get_content_list(self, cid):
		'''
			get content list
			args:
				cid: category id
			return:
				content_list list[{},{},...]
		'''
		time_now = str(int(time.time()))
		content_type = '1,2,4,3'
		page = "1"
		op = "2"
		url = "http://api.1sapp.com/content/getList?"
		params = "OSVersion=4.4.2&cid="+str(cid)+"&content_type="+content_type+"&deviceCode="+self.device_code+"&dtu=004&lat="+self.lat+"&lon="+self.lon+"&network=wifi&op="+op+"&page="+page+"&show_time=1489897727&time="+time_now+"&token="+self.token+"&uuid="+self.uuid1+"&version=20200"
		sign = self.get_sign(params)
		url = url+params+"&sign="+sign
		headers = {
			"User-Agent": "qukan_android",
			"Host": "api.1sapp.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		res = requests.get(url, headers=headers)
		content_list = json.loads(res.text)['data']['data']
		return content_list
	
	
	
	def get_content(self, content_id):
		'''
			get content
			args:
				content_id
			return:
				content list[{},] only one
		'''
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/content/getContent?"
		params = "OSVersion=4.4.2&content_id="+content_id+"&deviceCode="+self.device_code+"&dtu=004&from=1&lat="+self.lat+"&lon="+self.lon+"&network=wifi&time="+time_now+"&token="+self.token+"&uuid="+self.uuid1+"&version=20200"
		sign = self.get_sign(params)
		url = url+params+"&sign="+sign
		headers = {
			"User-Agent": "qukan_android",
			"Host": "api.1sapp.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		res = requests.get(url, headers=headers)
		data = json.loads(res.text)['data']
		return data

	def get_content_view(self, key):
		'''
			view a content
			args:
				the key of content
			return:
				result 
				example:
					Zepto1489901565126({"code":0,"message":"成功","currentTime":1489910517,"data":{"amount":10,"status_code":0}})
		'''
		time_now = str(int(time.time()))
		ua = "mozilla/5.0 (linux; android 4.4.2; gt-n7100 build/kot49h) applewebkit/537.36 (khtml, like gecko) version/4.0 chrome/30.0.0.0 mobile safari/537.36 qukan_android"
		url = "http://api.1sapp.com/content/view?cb=Zepto1489901565125&dtu=200&ua="+ua+"&key="+key+"&token="+self.token+"&_="+time_now
		
		headers = {
			"Host": "api.1sapp.com",
			"Connection": "keep-alive",
			"Accept": "*/*",
			"User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; GT-N7100 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 qukan_android",
			"Accept-Encoding": "gzip,deflate",
			"Accept-Language": "zh-CN,en-US;q=0.8",
			"Cookie": "UM_distinctid=15adf45bbb8a27-0ae9d06aa-126e710f-4b000-15adf45bbea408; qk=5573044; Hm_lvt_11aa3ce969914b5b5b7e49fc8259981b=1489804601; Hm_lpvt_11aa3ce969914b5b5b7e49fc8259981b=1489827174",
			"X-Requested-With": "com.jifen.qukan"
		}
		
		res = requests.get(url, headers=headers)
		return res.text

	def get_content_read(self, key):
		'''
			read content
			args:
				the key of content
		'''
		time_now = str(int(time.time()))
		ua = "mozilla/5.0 (linux; android 4.4.2; gt-n7100 build/kot49h) applewebkit/537.36 (khtml, like gecko) version/4.0 chrome/30.0.0.0 mobile safari/537.36 qukan_android"
		url = "http://api.1sapp.com/content/read?cb=Zepto1489901565126&dtu=200&ua="+ua+"&member_id="+self.member_info['member_id']+"&key="+key+"&token="+self.token+"&_="+time_now
		headers = {
			"Host": "api.1sapp.com",
			"Connection": "keep-alive",
			"Accept": "*/*",
			"User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; GT-N7100 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 qukan_android",
			"Accept-Encoding": "gzip,deflate",
			"Accept-Language": "zh-CN,en-US;q=0.8",
			"Cookie": "UM_distinctid=15adf45bbb8a27-0ae9d06aa-126e710f-4b000-15adf45bbea408; qk=5573044; Hm_lvt_11aa3ce969914b5b5b7e49fc8259981b=1489804601; Hm_lpvt_11aa3ce969914b5b5b7e49fc8259981b=1489827174",
			"X-Requested-With": "com.jifen.qukan"
		}
		
		
		res = requests.get(url, headers=headers)
		#print(res.text)
		return res.text
		
	def get_mission_pupil_list(self):
		'''
			get pupil list
		'''
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/mission/pupilIncomeNew?token="+self.token+"&dtu=200&limit=50&_="+time_now
		headers = {
			"Host": "api.1sapp.com",
			"Connection": "keep-alive",
			"Accept": "application/json",
			"Origin": "http://h5ssl.1sapp.com",
			"User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; GT-N7100 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 qukan_android",
			#"Referer": "http://h5ssl.1sapp.com/qukan_new2/dest/old_yq/inapp/old_yq/qd.html?v=20200&lat=40.41336&lon=116.671&network=wifi&dc="+self.device_code+"&dtu=004&uuid="+self.uuid1,
			"Accept-Encoding": "gzip,deflate",
			"Accept-Language": "zh-CN,en-US;q=0.8",
			"X-Requested-With": "com.jifen.qukan"
		}
		res = requests.get(url, headers=headers)
		print(res.text)
	'''
	##################################
	#           register
	##################################
	'''
	def get_captcha_get_img(self):
		'''
			get img
		'''
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/captcha/getImgCaptcha2?"
		params = "OSVersion=4.4.2&deviceCode="+self.device_code+"&dtu=004&lat="+self.lat+"&lon="+self.lon+"&network=wifi&time="+time_now+"&uuid="+self.uuid1+"&version=20200"
		sign = self.get_sign(params)
		url = url+params+"&sign="+sign
		headers = {
			"User-Agent": "qukan_android",
			"Host": "api.1sapp.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		
		res = requests.get(url, headers=headers)
		
		data = json.loads(res.text)['data']
		path = "tmp.jpeg"
		decode_png = base64.decodestring(data['data'].encode())
		#print(decode_png)
		with open(path, "wb") as f:
			f.write(decode_png)
			
		jz = JZ(path)
		code = jz.get_code()
		if code:
			return data['id'], code
		else:
			return data['id'], None
		#print(res.text)
	
	def get_captcha_get_sms(self, img_captcha_id, img_captcha):
		'''
			get sms
		'''
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/captcha/getSmsCaptcha?"
		params = "OSVersion=4.4.2&deviceCode="+self.device_code+"&dtu=004&img_captcha="+img_captcha+"&img_captcha_id="+img_captcha_id+"&lat="+self.lat+"&lon="+self.lon+"&network=wifi&telephone="+self.telephone+"&time="+time_now+"&use_way=1&uuid="+self.uuid1+"&version=20200"
		sign = self.get_sign(params)
		url = url+params+"&sign="+sign
		headers = {
			"User-Agent": "qukan_android",
			"Host": "api.1sapp.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		
		res = requests.get(url, headers=headers)
		print(res.text)
		data = json.loads(res.text)
		return data['code']
		
		
	def post_member_register(self, captcha):
		'''
			register a user
		'''
		url = "http://api.1sapp.com/member/register"
		headers = {
			"User-Agent": "qukan_android",
			"Host": "api.1sapp.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		time_now = str(int(time.time()))
		data = {
			"OSVersion": "4.4.2",
			"captcha": captcha,
			"deviceCode": self.device_code,
			"dtu": "004",
			"lat": self.lat,
			"lon": self.lon,
			"network": "wifi",
			"password": "123456",
			"telephone": self.telephone,
			"time": time_now,
			"uuid": self.uuid1,
			"version": "20200"
		}
		params = ""
		for key,value in data.items():
			params += key+"="+value+"&"
		sign = self.get_sign(params[0:-1])
		data['sign'] = sign
		res = requests.post(url, headers=headers, data=data)
		#print(res.text)
		data = json.loads(res.text)
		self.token = data['data']['token']
		return data['data']
		
	
	def post_member_invite_code(self, invite_code="A5573044"):
		'''
			add invite code
			A5573044
			A5571430
		'''
		time_now = str(int(time.time()))
		url = "http://api.1sapp.com/member/inviteCode?_="+time_now
		headers = {
			"Host": "api.1sapp.com",
			"Connection": "keep-alive",
			"Accept": "application/json",
			"Origin": "http://h5ssl.1sapp.com",
			"User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; GT-N7100 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 qukan_android",
			#"Referer": "http://h5ssl.1sapp.com/qukan_new2/dest/old_yq/inapp/old_yq/qd.html?v=20200&lat=40.41336&lon=116.671&network=wifi&dc="+self.device_code+"&dtu=004&uuid="+self.uuid1,
			"Accept-Encoding": "gzip,deflate",
			"Accept-Language": "zh-CN,en-US;q=0.8",
			"X-Requested-With": "com.jifen.qukan"
		}
		data = {
			"token": self.token,
			"invite_code": invite_code,
			"dtu": "200"
		}
		
		res = requests.post(url, headers=headers, data=data)
		#print(res.text)
		data = json.loads(res.text)
		return data
		
def register_user(invite_index):
	'''
		register a user
	'''
	ym = YIMA()
	#1. login ym
	time.sleep(1)
	ym.login_yima()
	#2. get a mobile
	time.sleep(1)
	mobile = ym.get_mobile()
	print("mobile: {}".format(mobile))
	#3. create a qtt
	device_code = gen_imme()
	qtt = QTT(mobile, device_code)
	code = -1
	while  code != 0:
		#4. get img captcha
		captcha = None
		while captcha is None:
			time.sleep(3)
			id, captcha = qtt.get_captcha_get_img()
			print("id:{} captcha:{}".format(id, captcha))
		#5. get sms
		time.sleep(3)
		code = qtt.get_captcha_get_sms(id, captcha)
		if code == -103:
			exit(-1)
	#6. get sms code
	sms_code = ym.get_code()
	#7. register
	time.sleep(1)
	data = qtt.post_member_register(sms_code)
	print("register result:{}".format(data))
	time.sleep(2)
	qtt.get_member_info()
	member_info = qtt.member_info
	data = [(member_info['member_id'], member_info['telephone'], member_info['balance'],
				member_info['coin'], member_info['invite_code'], member_info['teacher_id'],
				device_code)]
	uis.save(data)
	
	data = [(member_info['member_id'],)]
	uis.save_flag(data)
	#8. add invite
	time.sleep(4)
	invite_codes = ["A5573044", "A5571430"]
			
	data = qtt.post_member_invite_code(invite_codes[invite_index])
	print("add master result:{}".format(data))
	
	
class MyThread(threading.Thread):
	'''
		Thread
	'''
	delay = 8
	def __init__(self, name, iter_num):
		'''
			init a thread
		'''
		threading.Thread.__init__(self)
		self.name = "Thread-"+name
		self.num = iter_num
	
	def run(self):
		'''
			Main
		'''
		global lock, uis
		for i in range(self.num):
			print("{} {} times start....".format(self.name, i))
			print("{} 1. get channel list".format(self.name))
			#qqt.get_content_channel_list()
			if lock.acquire():
				print("{} {} times get a user".format(self.name, i))
				# read a user and update flag
				user = uis.get_one_user()
				if user:
					read_flag = [(1, 1, user[0])]
					uis.update_flag(read_flag)
				lock.release()
			if user:
				self.read_one_user(user)
			else:
				print("No User...")
			print("{} {} times end....".format(self.name, i))
		print("{} end....".format(self.name))
		
	def read_one_user(self, user):
		'''
			read a user
			args:
				user : user info
		'''
		try:
			qqt = QTT(str(user[1]), str(user[6]))
			#2. login
			time.sleep(2)
			print("{} 2. login tel: {}  device: {}".format(self.name, user[1], user[6]))
			qqt.get_member_login()
			#3. get member info
			time.sleep(3)
			print("{} 3. get member info".format(self.name))
			qqt.get_member_info()
			time.sleep(2)
			mission_list = qqt.get_mission_list()
			#print(mission_list)
			daily_has_read_count = mission_list['daily'][0]['count']
			print("{} {} has already read {}".format(self.name, qqt.telephone, daily_has_read_count))
			sign_in_today = mission_list['signIn']['today']
			treasure_box_is_active = mission_list['treasureBox']['isActive']
			#print(mission_list)
			#4. sign in
			if not sign_in_today:
				time.sleep(1)
				print("{} 4. sign in".format(self.name))
				qqt.post_mission_signin()
			#5. open a box
			if treasure_box_is_active:
				time.sleep(3)
				print("{} 5. open a box".format(self.name))
				qqt.post_mission_receive_box()
			#6. read content
			time.sleep(3)
			print("{} 6. read content".format(self.name))
			
			total_read = qqt.read_list(12 - daily_has_read_count)
			print("{} read over. total read: {}".format(self.name, total_read))
			if lock.acquire():
				#update userinfo
				uis.update([(qqt.member_info['balance'], qqt.member_info['coin'], 
					qqt.member_info['member_id']
				)])
				#
				read_record = [(qqt.member_info['member_id'], int(time.time()), total_read)]
				uis.save_read_record(read_record)
				read_flag = [(2, 1, qqt.member_info['member_id'])]
				uis.update_flag(read_flag)
				lock.release()
		except:
			print("Exception, Sleep: {}".format(self.delay))
			time.sleep(self.delay)
			self.delay *= 2
			self.read_one_user(user)
		else:
			self.delay = 8
	

def luhn_check(num):
	'''
		check the num 
	'''
	digits = [int(x) for x in reversed(str(num))]
	check_sum = sum(digits[1::2]) + sum((dig//10 + dig%10) for dig in [2*el for el in digits[::2]])
	return (10-check_sum%10)%10
	
def gen_imme():
	'''
		get an imme
	'''
	TAC='867922'
	FAC='02'
	SNR=565583
	imme=TAC+FAC+str(SNR+random.randint(1,1000))
	return (imme+str(luhn_check(imme)))
	
def init_data():
	'''
		init data
	'''
	'''
	path = "data/123.txt"
	tel_list=[]
	with open(path) as fo:
		while 1:
			line = fo.readline()
			if not line:
				break
			tel_list.append(line[0:len(line)-1])
	'''
	tel_list = ["17085166274"]
	for tel in tel_list:
		device_code = gen_imme()
		qtt = QTT(tel, device_code)
		time.sleep(2)
		print("2. login {}".format(tel))
		qtt.get_member_login()
		#3. get member info
		time.sleep(2)
		print("3. get member info")
		qtt.get_member_info()
		member_info = qtt.member_info
		data = [(member_info['member_id'], member_info['telephone'], member_info['balance'],
					member_info['coin'], member_info['invite_code'], member_info['teacher_id'],
					device_code)]
		uis.save(data)
		
		data = [(member_info['member_id'],)]
		uis.save_flag(data)
		
		
	
def main_method(thread_num=1, iter_num=5):
	thread_list = []
	THREAD_NUM = thread_num
	ITER_NUM = iter_num
	for i in range(0, THREAD_NUM):
		mt = MyThread(str(i), ITER_NUM)
		mt.setDaemon(True)
		thread_list.append(mt)
	
	for t in thread_list:
		t.start()
	for t in thread_list:
		t.join()
		
	print("main is over...")
		
	
if "__main__" == __name__:
	if len(argv)>1:
		if argv[1] == "r":
			invite_index = int(argv[2])
			register_user(invite_index)
		elif argv[1].isdigit():
			main_method(int(argv[1]), int(argv[2]))
	else:
		main_method()
	#img_name = argv[1]
	#get_app_start()
	#get_app_get_config()
	#channel_list = get_content_channel_list()
	#get_content_list()
	#test_url()
	#get_app_config(token)
	#test_md5()
	#test_per()
	#test_uuid()
	#test_key()
	#test_amount()
	#test_pupil()
	#test_img()
	#test_ocr_one(img_name)
	#test_register()
	#main()
	#main_method()
	#init_data()
	#register_user()
#com.jifen.qukan.view.activity.JumpActivity