# -*- coding: UTF-8 -*-
import pymysql

class Database():
	"""用来操作MySQL数据库"""
	def __init__(self):
		# 打开数据库连接
		self.connect = pymysql.connect(host='localhost',user='root',db='music',port=3306,charset='utf8')
		self.connect.autocommit(False)

	def insert(self,music_list,index_list):
		# 使用cursor()方法获取操作游标 
		cursor = self.connect.cursor()
		for index in index_list:
			album_name = music_list[index]['album_name']
			audio_name = music_list[index]['audio_name']
			timelength = str(music_list[index]['timelength'])
			play_url = music_list[index]['play_url']
			sql_str = "insert into music values('"+audio_name+"','"+album_name+"','"+timelength+"','"+play_url+"')"
			try:
				cursor.execute(sql_str)
				self.connect.commit()
			except Exception as e:
				self.connect.rollback()
