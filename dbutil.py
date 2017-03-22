
import sqlite3
import os


class DBUtil(object):
	#数据库文件绝句路径
	DB_FILE_PATH = 'data/userinfo.db'
	#表名称
	TABLE_NAME = 'userinfo'
	#是否打印sql
	SHOW_SQL = False
	init_flag = True
		
	
	
	def __init__(self, path, table, show=False, flag=False):
		self.DB_FILE_PATH = path
		self.TABLE_NAME = table
		self.SHOW_SQL = show
		self.init_flag = flag
		
		if self.init_flag:
			userinfo_sql = '''CREATE TABLE IF NOT EXISTS `{}` (
				  `member_id` int(11) NOT NULL,
				  `telephone` varchar(20) NOT NULL,
				  `balance` varchar(20) NOT NULL,
				  `coin` int(11) DEFAULT 0,
				  `invite_code` varchar(10) DEFAULT NULL,
				  `teacher_id` int(11) DEFAULT 0,
				  `device_code` var(20) NOT NULL,
				   PRIMARY KEY (`member_id`)
				)'''.format(self.TABLE_NAME)
			conn = self.get_conn()
			self.create_table(conn, userinfo_sql)
			
			userread_sql = '''CREATE TABLE IF NOT EXISTS `userread` (
				  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
				  `member_id` int(11) NOT NULL,
				  `read_time` varchar(20) NOT NULL,
				  `read_count` int(11) DEFAULT 0,
				   FOREIGN KEY(member_id) REFERENCES userinfo(member_id)
				)'''
			conn = self.get_conn()
			self.create_table(conn, userread_sql)
			
			userflag_sql = '''CREATE TABLE IF NOT EXISTS `userflag` (
				  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
				  `member_id` int(11) NOT NULL,
				  `share_flag` int(2) DEFAULT 1,
				  `read_flag` int(2) DEFAULT 0,
				   FOREIGN KEY(`member_id`) REFERENCES `userinfo`(`member_id`)
				)'''
			conn = self.get_conn()
			self.create_table(conn, userflag_sql)
			self.init_flag = False
		
	
	def get_conn(self):
		'''获取到数据库的连接对象，参数为数据库文件的绝对路径
		如果传递的参数是存在，并且是文件，那么就返回硬盘上面改
		路径下的数据库文件的连接对象；否则，返回内存中的数据接
		连接对象'''
		conn = sqlite3.connect(self.DB_FILE_PATH)
		if os.path.exists(self.DB_FILE_PATH) and os.path.isfile(self.DB_FILE_PATH):
			#print('硬盘上面:[{}]'.format(self.DB_FILE_PATH))
			return conn
		else:
			conn = None
			print('内存上面:[:memory:]')
			return sqlite3.connect(':memory:')

	def get_cursor(self, conn):
		'''该方法是获取数据库的游标对象，参数为数据库的连接对象
		如果数据库的连接对象不为None，则返回数据库连接对象所创
		建的游标对象；否则返回一个游标对象，该对象是内存中数据
		库连接对象所创建的游标对象'''
		if conn is not None:
			return conn.cursor()
		else:
			return self.get_conn('').cursor()

	###############################################################
	####			创建|删除表操作	 START
	###############################################################
	def drop_table(self, conn, table):
		'''如果表存在,则删除表，如果表中存在数据的时候，使用该
		方法的时候要慎用！'''
		if table is not None and table != '':
			sql = 'DROP TABLE IF EXISTS ' + table
			if self.SHOW_SQL:
				print('执行sql:[{}]'.format(sql))
			cu = self.get_cursor(conn)
			cu.execute(sql)
			conn.commit()
			print('删除数据库表[{}]成功!'.format(table))
			self.close_all(conn, cu)
		else:
			print('the [{}] is empty or equal None!'.format(sql))

	def create_table(self, conn, sql):
		'''创建数据库表：userinfo'''
		if sql is not None and sql != '':
			cu = self.get_cursor(conn)
			if self.SHOW_SQL:
				print('执行sql:[{}]'.format(sql))
			cu.execute(sql)
			conn.commit()
			print('创建数据库表[{}]成功!'.format(self.TABLE_NAME))
			self.close_all(conn, cu)
		else:
			print('the [{}] is empty or equal None!'.format(sql))

	###############################################################
	####			创建|删除表操作	 END
	###############################################################

	def close_all(self, conn, cu):
		'''关闭数据库游标对象和数据库连接对象'''
		try:
			if cu is not None:
				cu.close()
		finally:
			if conn is not None:
				conn.close()

	###############################################################
	####			数据库操作CRUD	 START
	###############################################################

	def save(self, conn, sql, data):
		'''插入数据'''
		if sql is not None and sql != '':
			if data is not None:
				cu = self.get_cursor(conn)
				for d in data:
					if self.SHOW_SQL:
						print('执行sql:[{}],参数:[{}]'.format(sql, d))
					cu.execute(sql, d)
					conn.commit()
				self.close_all(conn, cu)
		else:
			print('the [{}] is empty or equal None!'.format(sql))

	def fetchall(self, conn, sql, data=()):
		'''查询所有数据'''
		if sql is not None and sql != '':
			cu = self.get_cursor(conn)
			if self.SHOW_SQL:
				print('执行sql:[{}]'.format(sql))
			if data:
				cu.execute(sql, data)
			else:
				cu.execute(sql)
			r = cu.fetchall()
			return r
		else:
			print('the [{}] is empty or equal None!'.format(sql)) 
			return []
			

	def fetchone(self, conn, sql, data):
		'''查询一条数据'''
		if sql is not None and sql != '':
			if data is not None:
				#Do this instead
				d = (data,) 
				cu = self.get_cursor(conn)
				if self.SHOW_SQL:
					print('执行sql:[{}],参数:[{}]'.format(sql, data))
				cu.execute(sql, d)
				r = cu.fetchall()
				return r
				# if len(r) > 0:
					# for e in range(len(r)):
						# print(r[e])
			else:
				print('the [{}] equal None!'.format(data))
				return []
		else:
			print('the [{}] is empty or equal None!'.format(sql))
			return []

	def update(self, conn, sql, data):
		'''更新数据'''
		if sql is not None and sql != '':
			if data is not None:
				cu = self.get_cursor(conn)
				for d in data:
					if self.SHOW_SQL:
						print('执行sql:[{}],参数:[{}]'.format(sql, d))
					cu.execute(sql, d)
					conn.commit()
				self.close_all(conn, cu)
		else:
			print('the [{}] is empty or equal None!'.format(sql))

	def delete(self, conn, sql, data):
		'''删除数据'''
		if sql is not None and sql != '':
			if data is not None:
				cu = self.get_cursor(conn)
				for d in data:
					if self.SHOW_SQL:
						print('执行sql:[{}],参数:[{}]'.format(sql, d))
					cu.execute(sql, d)
					conn.commit()
				self.close_all(conn, cu)
		else:
			print('the [{}] is empty or equal None!'.format(sql))
	###############################################################
	####			数据库操作CRUD	 END
	###############################################################

