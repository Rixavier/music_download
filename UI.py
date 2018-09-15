# -*- coding:UTF-8 -*-
import sys
from PyQt5.QtWidgets import (QMainWindow,QApplication,QLineEdit,QComboBox,QPushButton,QMessageBox,QTableWidget,QTableWidgetItem,QProgressBar,QFrame)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QSize,Qt)
from Logic import QQMusic
from Logic import KuGouMusic
from DataBase import Database

class UI(QMainWindow):
	"""主界面类"""
	def __init__(self):		
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setGeometry(600,280,900,500)
		self.setWindowTitle("基于Python的网络音乐爬虫系统")
		self.setWindowIcon(QIcon("image/logo.jpg"))
		self.setFixedSize(self.width(), self.height()) 
		#设置状态栏
		self.status_bar = self.statusBar()
		#设置进度条
		self.progress_bar = QProgressBar(self.status_bar)
		self.progress_bar_css()
		self.progress_bar.hide()
		#类的属性
		self.music_list = []
		self.search_engine = ''
		#设置text文本框
		self.text_search = QLineEdit(self)
		self.text_search_css()
		#设置搜索按钮
		self.btn_search = QPushButton("搜索",self)
		self.btn_search_css()
		self.btn_search.clicked.connect(self.btn_search_clicked)
		#设置搜索结果表格
		self.table_result = QTableWidget(self)
		self.table_result_css()
		self.table_result.hide()
		#设置下载按钮
		self.btn_download = QPushButton("下载",self)
		self.btn_download_css()
		self.btn_download.clicked.connect(self.btn_download_clicked)
		self.btn_download.hide()

		self.show()

	def text_search_css(self):
		self.text_search.setGeometry(270,20,200,30)
		self.text_search.setStyleSheet('''
			padding: 6px 12px; 
			font-size: 14px; 
			line-height: 1.428571429; 
			color: #555555; 
			vertical-align: middle; 
			background-color: #ffffff; 
			border: 1px solid #cccccc; 
			border-radius: 4px; 
			border-color: #66afe9; 
		''')
	
	def btn_search_css(self):
		self.btn_search.setGeometry(550,20,50,30)
		self.btn_search.setShortcut('Ctrl+D')
		self.btn_search.setStyleSheet('''
			font-size:12px;
			border: 1px solid #cccccc; 
			border-radius: 4px; 
			border-color: #1B9AF7; 
			''')

	def table_result_css(self):	
		#设置表格属性
		self.table_result.setGeometry(42,100,821,300)
		self.table_result.setColumnCount(3)
		self.table_result.setHorizontalHeaderLabels(['歌曲名','专辑','时长'])
		self.table_result.horizontalHeader().resizeSection(0,400)
		self.table_result.horizontalHeader().resizeSection(1,300)
		self.table_result.horizontalHeader().resizeSection(2,100)
		self.table_result.setEditTriggers(QTableWidget.NoEditTriggers)
		self.table_result.setSelectionBehavior(QTableWidget.SelectRows)
		self.table_result.setSelectionMode(QTableWidget.MultiSelection)
		self.table_result.verticalHeader().setVisible(False)
		self.table_result.setFrameShape(QFrame.Box)

	def table_result_edit(self,music_list):
		'''对搜索结果以表格形式展示'''
		self.table_result.setRowCount(len(music_list))
		#填充表格内容
		for i in range(0,len(music_list)):
			self.table_result.setItem(i,0,QTableWidgetItem(music_list[i]["audio_name"]))
			self.table_result.setItem(i,1,QTableWidgetItem(music_list[i]["album_name"]))			
			time = int(music_list[i]["timelength"]/1000)
			minute = int(time / 60)
			second = int(time % 60)
			self.table_result.setItem(i,2,QTableWidgetItem('%02d:%02d' %(minute,second)))
		self.progress_bar.hide()
		self.table_result.show()
		self.btn_download.show()
	
	def btn_download_css(self):
		self.btn_download.setGeometry(425,430,50,30)
		self.btn_download.setStyleSheet('''
			padding: 6px 12px; 
			font-size: 14px; 
			line-height: 1.428571429; 
			color: #555555; 
			vertical-align: middle; 
			background-color: #ffffff; 
			border: 1px solid #cccccc; 
			border-radius: 4px; 
			border-color: #66afe9; 
		''')

	def progress_bar_css(self):
		self.progress_bar.setOrientation(Qt.Horizontal)
		self.progress_bar.setGeometry(10,0,120,18)
		self.progress_bar.setStyleSheet(
			"QProgressBar{text-align:center;border:2px solid grey;border-radius:4px;}"
			"QProgressBar::chunk {background-color:#11A0FF;width:10px;margin:0.5px;}"
		)

	def btn_search_clicked(self):
		keyword = self.text_search.text()
		self.progress_bar.show()
		kugoumusic = KuGouMusic()
		result = kugoumusic.search_music_list(keyword)
		result = kugoumusic.search_music_info(result,self)
		self.music_list = result[:]
		self.table_result_edit(result[:])
		
	def btn_download_clicked(self):
		download_index = []
		selected_items = self.table_result.selectedItems()
		for item in selected_items:
			index  = self.table_result.indexFromItem(item).row()
			if index not in download_index:
				download_index.append(index)
		#控制台输出要下载的index列表
		print(download_index)
		#进行下载
		self.progress_bar.show()
		kugoumusic = KuGouMusic()
		kugoumusic.download(self.music_list,download_index,self)
		#保存到数据库中
		db = Database()
		db.insert(self.music_list,download_index)
		self.progress_bar.hide()
		QMessageBox.information(self,'提示','下载成功！')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	UI = UI()
	sys.exit(app.exec_())
	