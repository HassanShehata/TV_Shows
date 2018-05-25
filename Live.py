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
		f= open('channels.txt','r')
		for line in f.readlines():
			channels_pool.append(line)
		f.close()

	elif mode == 'write':
		for i in results:
			j=j+'      "'+i.split(":")[0]+'":"'+i.split(":")[1]+'",\n'
		f= open('Live_data.json','w')
		f.write("{\n \"live\":\n    [{\n"+j[:-2]+"\n   }]\n}")
		



def fetch(url):
	browser.get(url)
	soup= bs(browser.page_source, "lxml")
	return soup


def general(name,ch,tag,info):

	soup=fetch(ch)
	flag=len(info.split(","))

	if  flag == 2:
		result=soup.find(tag,{info.split(",")[0]:info.split(",")[1]}).text
		print(name+":"+result)
		results.append(name+":"+result)

	elif len(info) == 1:
		result=soup.find_all(tag)[int(info)].text
		print(name+":"+result)
		results.append(name+":"+result)

	"""
	elif flag == 5:
		result=soup.find(tag,{info.split(",")[0]:info.split(",")[1]}).text
		result=soup.find(info.split(",")[2],{info.split(",")[3]:info.split(",")[4]}).text
		print(name+":"+result)
	"""


def main():
	file_handler("read")
	for i in channels_pool:
		general(i.split("*")[0],i.split("*")[1],i.split("*")[2],i.strip('\n').split("*")[3])
	file_handler("write")
	

main()
browser.close()
