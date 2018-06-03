#!/usr/bin/python3

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import json
import time


browser = webdriver.Firefox(executable_path='./geckodriver')
channels_pool=[]
results=[]


def file_handler(mode):

	j=""
	if mode == 'read':
		f= open('channels_programs.txt','r')
		for line in f.readlines():
			channels_pool.append(line)
		f.close()

	elif mode == 'write':
		for i in results:
			j=j+i
		f= open('program_data.json','w')
		f.write("{\n \"channels-programs\":\n"+j[:-1]+"\n}")
		

def general(name,ch):

	constract=""
	if name.split('-')[0] == 'mbc':
		browser.get(ch)
		soup= bs(browser.page_source, "lxml")
		page=soup.find_all("div",{"class":"teaser length-2halfhour"})
		
		for data in page:
			#data_soup= bs(data,"lxml")
			prog_name=data.find("h2").text
			time=data.find("ul",{"class":"time time-2"}).text.strip("\n")
			image="http://www.mbc.net"+data.find("img")['src']
			constract=constract+("     \"prog_name\":\""+prog_name+"\"[{\n          \"time\":\""+time+"\",\n          \"image\":\""+image+"\"\n     }],")

		results.append("[{\n \""+name+"\":\n     [{\n"+constract[:-1]+"\n}],")


def main():

	file_handler("read")
	for i in channels_pool:
		general(i.split("*")[0],i.strip('\n').split("*")[1])
	file_handler("write")
	

main()
browser.close()
