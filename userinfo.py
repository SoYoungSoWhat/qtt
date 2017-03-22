from dbutil import DBUtil
import time
from sys import argv
class UserInfoService(object):
	'''
		提供对数据库操作的接口
		1.save(data)
		2.save_flag(data)
		3.save_read_record(data)
		4.update(data)
		5.update_flag(data)
		6.update_all_flag(data)
		7.get_all()
		8.get_all_user_read()
		9.get_all_user_flag(read_flag, share_flag)
		12.get_register()
	'''
	def __init__(self):
		'''初始化数据库信息'''
		path = 'data/userinfo.db'
		table = 'userinfo'
		self.db = DBUtil(path, table)
		
	def save(self, data):
		'''
			保存一条用户信息
			
			data = [(member_id (int), telephone (string),  
					balance(string), invite_code(string), coin(int), 
					teacher_id(int), device_code(string))]
		'''
		save_sql = '''INSERT INTO userinfo 
			(member_id, telephone, balance, coin, invite_code, teacher_id, device_code
			) 
			VALUES 
			(?, ?, ?, ?, ?, ?, ?)
		'''
		conn = self.db.get_conn()
		self.db.save(conn, save_sql, data)
		
	def save_flag(self, data):
		'''
			保存一条用户标志
			
			args: data = [(member_id(int),)]
		'''
		save_sql = '''INSERT INTO userflag
				(member_id) VALUES (?)
			'''
		conn = self.db.get_conn()
		self.db.save(conn, save_sql, data)
	
	def save_read_record(self, data):
		'''
			保存一条用户阅读信息
			
			arg: data = [(member_id(int), read_time(string), read_count(int))]
		'''
		save_sql = '''INSERT INTO userread
				(member_id, read_time, read_count)
				VALUES
				(?, ?, ?)
			'''
		conn = self.db.get_conn()
		self.db.save(conn, save_sql, data)
	
	def update(self, data):
		'''
			更新一条用户信息
			
			data = [balance(string), coin(int), (member_id(int)]
		'''
		update_sql = '''UPDATE userinfo 
					SET balance=?, coin=?
					WHERE member_id=?
				'''
		conn = self.db.get_conn()
		self.db.update(conn, update_sql, data)
		
	def update_flag(self, data):
		'''
			更新一条flag信息
			
			data = [read_flag(int{0,1,2}), share_flag(int {0, 1})), (member_id(int)]
		'''
		update_sql = '''UPDATE userflag
					SET read_flag=?, share_flag=?
					WHERE member_id=?
				'''
		conn = self.db.get_conn()
		self.db.update(conn, update_sql, data)
		
	def update_all_flag(self):
		'''
			更新所有read_flag信息
		'''
		update_sql = ''' UPDATE userflag
					SET read_flag=?
				'''
		conn = self.db.get_conn()
		self.db.update(conn, update_sql, [(0,)])


	def get_all(self):
		'''
			查询所有用户信息
		'''
		sql = '''SELECT * FROM userinfo'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql)
		return res
	
	def get_all_user_read(self):
		'''
			查询所有read_record
		'''
		sql = '''SELECT * FROM userread'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql)
		return res
		
	def get_all_user_flag(self, read_flag, share_flag=1):
		'''
			查询所有user_flag
			
			args: read_flag(0, 1, 2)
					share_flag(0, 1)
		'''
		sql = '''SELECT * FROM userflag WHERE read_flag=? AND share_flag=?'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql, (read_flag, share_flag))
		return res
	
	def get_one(self, member_id):
		'''
			查询一条用户信息
			
			arg: member_id (int)
		'''
		sql = '''SELECT * FROM userinfo WHERE member_id=?'''
		conn = self.db.get_conn()
		res = self.db.fetchone(conn, sql, uid)
		
		if len(res)>0:
			return res[0]
		else:
			return None
			
	def get_user_mobile(self, telephone):
		'''
			查询一条用户信息
			
			arg: telephone (string)
		'''
		sql = '''SELECT * FROM userinfo WHERE telephone=?'''
		conn = self.db.get_conn()
		res = self.db.fetchone(conn, sql, telephone)
		
		if len(res)>0:
			return res
		else:
			return []
	
	def get_register(self):
		'''
			查询注册用户
		'''
		sql = ''' SELECT * FROM userinfo ui, userflag uf
				WHERE ui.member_id = uf.member_id AND uf.share_flag=0
			'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql)
		if len(res)>0:
			return res
		else:
			return []
	
	def get_one_user(self):
		'''
			查询一条flag=0的用户信息
		'''
		
		sql = '''SELECT * 
			FROM userinfo ui, userflag uf
			WHERE ui.member_id = uf.member_id AND uf.read_flag = 0 AND uf.share_flag=1
		'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql)
		if len(res)>0:
			return res[0]
		else:
			return None
	
	def get_all_already_read_user(self):
		'''
			查询已完成的用户
		'''
		sql = '''SELECT * 
			FROM userinfo ui, userflag uf
			WHERE ui.member_id = uf.member_id AND uf.read_flag = 2 AND uf.share_flag=1
		'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql)
		return res
		
	def get_all_not_read_user(self):
		'''
			查询未完成的用户
		'''
		sql = '''SELECT * 
			FROM userinfo ui, userflag uf
			WHERE ui.member_id = uf.member_id AND uf.read_flag = 0 AND uf.share_flag=1
		'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql)
		return res
		
	def get_all_reading_user(self):
		'''
			查询正在完成的用户
		'''
		sql = '''SELECT * 
			FROM userinfo ui, userflag uf
			WHERE ui.member_id = uf.member_id AND uf.read_flag = 1 AND uf.share_flag=1
		'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql)
		return res
	
	def get_user_read_count(self, member_id):
		'''
			查询用户的阅读量
		'''
		time_ms = int(time.time())
		time_local = time.localtime(time_ms)
		time_format = "%Y-%m-%d"
		time_str = time.strftime(time_format, time_local)
		time_local = time.strptime(time_str, time_format)
		time_ms = int(time.mktime(time_local))
		#print("今日00:00对应毫秒:{}".format(time_ms))
		sql = '''SELECT sum(read_count) FROM userread
				WHERE member_id = ? AND read_time > ?
			'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql, (member_id, time_ms))
		if res[0][0]:
			return res[0][0]
		else:
			return 0
		
	def get_user_coin(self, coin):
		'''
			查询一定coin的用户
		'''
		sql = '''SELECT * FROM userinfo
				WHERE coin >= ?'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql, (score,))
		return res
		
	def get_user_balance(self, balance):
		'''
			查询一定balance的用户
		'''
		sql = '''SELECT * FROM userinfo
				WHERE balance == ?'''
		conn = self.db.get_conn()
		res = self.db.fetchall(conn, sql, (balance,))
		return res
	
	def get_time_str(self, time_ms, time_format="%Y-%m-%d"):
		'''
			毫秒-->指定格式
		'''
		time_local = time.localtime(time_ms)
		time_str = time.strftime(time_format, time_local)
		return time_str

if __name__ == "__main__":
	uis = UserInfoService()
	if len(argv)>1:
		if argv[1] == "clear":
			uis.update_all_flag()
		elif argv[1] == "coin":
			res = uis.get_user_score(argv[2])
			for user in res:
				print("Tel: {},  Balance: {}, Coin:{} Invite Code: {}".format(user[1], user[2], user[3], user[4]))
		elif argv[1] == "balance":
			res = uis.get_user_balance(argv[2])
			for user in res:
				print("Tel: {},  Balance: {}, Coin:{} Invite Code: {}".format(user[1], user[2], user[3], user[4]))
		elif argv[1] == "tel":
			res = uis.get_user_mobile(argv[2])
			for user in res:
				print("Mobile: {},  Balance: {}, Coin:{} Invite Code: {}".format(user[1], user[2], user[3], user[4]))
		elif argv[1] == "all":
			all_user = uis.get_all()
			for user in all_user:
				print("Mobile: {},  Balance: {}, Coin:{} Invite Code: {}".format(user[1], user[2], user[3], user[4]))
	else:
		all_user = uis.get_all()
		#for user in all_user:
		#	print(user)
		already_user = uis.get_all_already_read_user()
		not_user = uis.get_all_not_read_user()
		reading_user = uis.get_all_reading_user()
		register_user = uis.get_register()
		
		print("一共有用户: {}".format(len(all_user)))
		print("已经完成: {} 完成比例: {:.3f}".format(len(already_user), len(already_user)/len(all_user)))
		print("未完成: {}".format(len(not_user)))
		print("正在进行: {}".format(len(reading_user)))
		for user in reading_user:
			res = uis.get_user_read_count(user[0])
			if res < 12:
				uis.update_flag([(0, 1, user[0])])
			else:
				uis.update_flag([(2, 1, user[0])])
			print("User:{} has already reads {}".format(user[1], res))
		#print("注册用户:{}".format(len(register_user)))
		#for user in register_user:
		#	print("Tel:{}, Invite Code:{}".format(user[1], user[4]))
		
	
	