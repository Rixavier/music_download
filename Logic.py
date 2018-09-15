# -*- coding:UTF-8 -*-
from urllib import request
from urllib import parse
from urllib.request import urlretrieve
import json
import re
import os
import time

class QQMusic(object):
	"""download from QQMusic"""
	def __init__(self):
		self.url = "https://y.ruhaowu.com/qqmusic/soso"
		self.header = {
			'origin':
			'https://y.ruhaowu.com',
			'referer':
			'https://y.ruhaowu.com//',
			'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
			}

	def search(self,search_str):
		'''根据search_str查询歌曲'''
		#构造post数据
		form_data = {}
		form_data['name'] = search_str
		data = parse.urlencode(form_data).encode("UTF-8")
		#创建Request对象
		request_obejct = request.Request(url=self.url,data=data,headers=self.header)
		resopnse_object = request.urlopen(request_obejct)
		json_result = resopnse_object.read().decode("UTF-8")
		result = json.loads(json_result)
		#控制台显示搜索的结果
		for item in result:
			print(item['name'])
			print(item['singer'])
			print(item['album'])
			print(item['MP3'])
			print('***********************************************************************************************')
		return result

	def download(self,result,limit):
		'''根据所给参数下载歌曲'''
		count = 0
		flag = True
		#创建文件夹
		if 'QQ音乐下载' not in os.listdir():
			os.makedirs('QQ音乐下载')
		for item in result:
			if flag==True:
				mp3_name = item['name']+' - '+item['singer']+'.mp3'
				#下载歌曲并给歌曲命名
				urlretrieve(url=item['MP3'],filename='QQ音乐下载/'+mp3_name)
				count += 1
				time.sleep(3)
			if count==limit:
				flag=False
		
class KuGouMusic(object):
	"""download for KuGouMusic"""
	def __init__(self):
		self.url_list = 'http://songsearch.kugou.com/song_search_v2?'
		self.url_music = 'http://www.kugou.com/yy/index.php?'
		self.headers = {
			'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
			}

	def search_music_list(self,keyword):
		'''根据关键字keyword来搜索歌曲，并返回一个包含albumid和filehash的列表'''
		#Get方式提交的数据
		form_data = {}
		form_data['callback'] = 'jQuery1124049371189518558833_1525014005109'
		form_data['keyword'] = keyword
		form_data['page'] = '1'
		form_data['pagesize'] = '30'
		form_data['userid'] = '-1'
		form_data['clientver'] = '' 
		form_data['platform'] = 'WebFilter'
		form_data['tag'] = 'em'
		form_data['filter'] = '2'
		form_data['iscorrection'] = '1'
		form_data['privilege_filter'] = '0'
		form_data['_'] = '1525014005111'
		data = parse.urlencode(form_data)
		#拼接url
		url = self.url_list + data
		request_object = request.Request(url=url,headers=self.headers)
		response_object = request.urlopen(request_object)
		str_text = response_object.read().decode('UTF-8')
		#正则表达式匹配albumid和filehash
		pattern_albumid = re.compile(r'"AlbumID":"[0-9]*"')
		pattern_filehash = re.compile(r'"FileHash":"[0-9A-Z]*"')
		list_albumid = pattern_albumid.findall(str_text)
		list_filehash = pattern_filehash.findall(str_text)
		#将list_albumid和list_filehash拼接成一个列表返回
		music_list = []
		for i in range(0,len(list_albumid)):
			music_str = '{'+list_albumid[i]+','+list_filehash[i]+'}'
			music_dirt = eval(music_str)
			music_list.append(music_dirt)
		return music_list
	
	def search_music_info(self,music_list,UI):
		'''根据搜索到的歌曲列表，来查询具体每首歌的audio_name、album_name、timelength、play_url,返回列表'''
		UI.progress_bar.setMinimum(0)
		UI.progress_bar.setMaximum(len(music_list))
		return_music_list = []
		for i in range(0,len(music_list)):
			#Get方式提交的数据
			form_data = {}
			form_data['r'] = 'play/getdata'
			form_data['hash'] = music_list[i]['FileHash']
			form_data['album_id'] = music_list[i]['AlbumID']
			form_data['_'] = '1525073083956'
			data = parse.urlencode(form_data)
			#拼接url
			url = self.url_music + data
			request_object = request.Request(url=url,headers=self.headers)
			response_object = request.urlopen(request_object)
			json_music_info = response_object.read().decode('UTF-8')
			dict_music_info = json.loads(json_music_info)
			#控制台输出歌曲信息
			print(dict_music_info['data']['audio_name'])
			print(dict_music_info['data']['album_name'])
			print(dict_music_info['data']['timelength'])
			print(dict_music_info['data']['play_url'])
			print('*********************************************************************************************************************')
			#将歌曲信息整理成字典添加到return_music_list列表中
			str_single_music_info = '{"audio_name":"' + dict_music_info['data']['audio_name'] + '"}'
			dict_single_music_info = eval(str_single_music_info)
			dict_single_music_info['album_name'] = dict_music_info['data']['album_name']
			dict_single_music_info['timelength'] = dict_music_info['data']['timelength']
			dict_single_music_info['play_url'] = dict_music_info['data']['play_url']
			return_music_list.append(dict_single_music_info)
			time.sleep(1)
			#更新进度条
			UI.progress_bar.setValue(i+1)

		return return_music_list
	
	def download(self,music_list,index_list,UI):
		'''根据所给参数下载歌曲'''
		UI.progress_bar.setMinimum(0)
		UI.progress_bar.setMaximum(len(index_list))
		i = 0
		UI.progress_bar.setValue(i)
		#创建文件夹
		if '酷狗音乐下载' not in os.listdir():
			os.makedirs('酷狗音乐下载')
		for index in index_list:
			mp3_name = music_list[index]['audio_name']+'.mp3'
			#下载歌曲并给歌曲命名
			urlretrieve(url=music_list[index]['play_url'],filename='酷狗音乐下载/'+mp3_name)
			time.sleep(1)
			#更新进度条
			i = i + 1
			UI.progress_bar.setValue(i)

		
	