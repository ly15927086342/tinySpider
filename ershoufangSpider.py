#coding = 'utf-8'

import json
from lxml import etree
from bs4 import BeautifulSoup
import math
import sqlite3
import re
from spider import AbstractSpiderFrame

'''
模板方法模式，
继承AbstractSpiderFrame的子类，重写部分方法
'''
class ershoufangSpider(AbstractSpiderFrame):
	def __init__(self, regions = [], fields = [], thread_num = 3,dict_path = './'):
		super(ershoufangSpider, self).__init__(regions,fields,thread_num,dict_path)

	# @parms{region}: self.regions[i]
	# @return{childLink}：根据区域生成待爬取的主页链接
	def getEntryFunc(self,region):
		return 'http://wh.58.com/'+region+'/zufang/'

	# @parms{url}: self.entry[i]
	# @return{childLink}：self.entry[i]页获取的所有列表页的链接list
	def getPagesFunc(self,url):
		pg = []
		res = self.getHtml(url)
		soup = BeautifulSoup(res,'lxml')
		page = soup.find_all(class_='pager')[0]
		a = page.find_all('a')
		maxP = int(a[len(a)-2].find('span').string)
		for i in range(1,maxP+1):
			pg.append(url+'pn'+str(i)+'/')
		return pg

	# @parms{url}: self.pages[i]
	# @return{childLink/False}： self.pages[i]页所有待爬页面的链接list，如果页面异常，返回False
	def getLinkListFunc(self,url):
		res = self.getHtml(url)
		soup = BeautifulSoup(res,'lxml')
		childLink = []
		try:
			domItem = soup.find(class_='house-list-wrap').find_all(class_='list-info')
			for dom in domItem:
				link = dom.find(class_='title').find('a').get('href')
				# //开头转http://
				if(re.match(r'https:',link)==None):
					link = 'https:'+link
				# ?后面的参数都舍弃
				link = link.split('?')[0]
				childLink.append(link)
			return childLink
		except:
			return False

	# @parms{url}: self.links[i]
	# @return{record}: 和self.fields顺序必须保持一致，返回一个list，该list会写入csv
	# 详情页的爬取处理函数
	def processLinksFunc(self,url):
		res = self.getHtml(url)
		soup = BeautifulSoup(res,'lxml')
		record = []
		try:
			card_data = soup.find(class_='card-top')
			title = card_data.find(class_='card-title').find('i').string.strip().replace(' ','')
			price_warp = card_data.find(class_="price-wrap")
			er_list = card_data.find(class_="er-list")
			er_list_two = card_data.find(class_="er-list-two")
			list_one = er_list.find_all(class_="f-fl")
			list_two = er_list_two.find_all(class_="f-fl")
			price = price_warp.find(class_="price").string.strip().replace(' ','')
			unit = price_warp.find(class_="unit").string.strip().replace(' ','')
			type = list_one[0].find(class_='content').string.strip().replace(' ','')
			area = list_one[1].find(class_='content').string.strip().replace(' ','').replace('\xa0','')
			direction = list_one[2].find(class_='content').string.strip().replace(' ','')
			floor = list_one[3].find(class_='content').string.strip().replace(' ','')
			decoration = list_one[4].find(class_='content').string.strip().replace(' ','')
			community = list_two[0].find(class_='content').find('span').string.strip().replace(' ','')
			subway = list_two[1].find(class_='content').string.strip().replace(' ','')
			address = list_two[2].find(class_='content').string.strip().replace(' ','')
			description = soup.find(class_='describe').find(class_='item').string.strip().replace(' ','')
			loc = re.search(r'try{(.*?)}catch',res.replace(' ','').replace('\n','')).group(0).split(';')
			bdlat = loc[1][19:-1]
			bdlng = loc[2][19:-1]
			record = [title,price,unit,type,area,direction,floor,decoration,community,subway,address,bdlat,bdlng,description]
		except:
			pass
		return record