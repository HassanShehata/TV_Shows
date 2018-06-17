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
		f.write("{\n \"channels-programs\":\n"+j+"\n}")
		

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
			desc_link="http://www.mbc.net"+data.find("a")['href']

			if desc_link.split("/")[5]=="articles":
				print(desc_link)
				
				try:
					browser.get(desc_link)
				except Message:
					browser.refresh()
					pass
				
				if bs(browser.page_source, "lxml"):
					print(1)
					soup= bs(browser.page_source, "lxml")
					desc= ""
					for n in soup.find_all("p")[3:9]:
						desc=desc+n.text
					desc=desc.replace("\""," ")
					#print(desc)
				else:
					print(0)
					desc=" "
				constract=constract+("     \"prog_name\":\""+prog_name+"\"[{\n          \"time\":\""+time+"\",\n          \"image\":\""+image+"\",\n          \"description\":\""+desc.strip("\n")+"\"\n     }],")

			else:

				desc_link="http://www.mbc.net"+data.find("a")['href'].split(".")[0]+"/about-and-stars.html"
				print(desc_link)

				try:
					browser.get(desc_link)
				except Message:
					browser.refresh()
					pass

				soup= bs(browser.page_source, "lxml")
				try:
					soup.find("div",{"class":"arena"}).text
					print(1)
					desc= soup.find("div",{"class":"arena"}).text
					desc=desc.replace("\""," ")
					#print(desc)
				except AttributeError:
					print(0)
					desc=" "
					pass

				constract=constract+("     \"prog_name\":\""+prog_name+"\"[{\n          \"time\":\""+time+"\",\n          \"image\":\""+image+"\",\n          \"description\":\""+desc.strip("\n")+"\"\n     }],")
				
		results.append("[{\n \""+name+"\":\n     [{\n"+constract[:-1]+"\n}]\n")


def osn(name,ch):

	channel_detector=["0"]
	constract=""
	if name.split('-')[0] == 'osn':
		browser.get(ch)
		#actions= ActionsChains(browser)
		for i in range(2):
			test= browser.find_elements_by_class_name("tv-show-title-ch-1")
			#test= soup.find_all("div",{"class":"tv-show-title-ch-1"})	
			for n in test:
				n.click()
				time.sleep(2)
				soup= bs(browser.page_source, "lxml")
				channel= browser.find_element_by_xpath("/html/body/form/div[15]/div/div/div[2]/div[1]/div/img").get_attribute("src")
				name= soup.find("div",{"tv-popup-h2"}).text
				show_time= browser.find_element_by_xpath("/html/body/form/div[15]/div/div/div[2]/div[2]/div[2]/div[3]").text
				duration= browser.find_element_by_xpath("/html/body/form/div[15]/div/div/div[2]/div[2]/div[2]/div[4]").text
				image= browser.find_element_by_xpath("/html/body/form/div[15]/div/div/div[2]/div[2]/div[1]/img").get_attribute("src")
				desc= browser.find_element_by_xpath("/html/body/form/div[15]/div/div/div[2]/div[3]/p").text
				constract=constract+"[{\n          \"channel\":\""+channel+"\",\n          \"name\":\""+name+"\",\n          \"time\":\""+show_time+"\",\n          \"duration\":\""+duration+"\",\n          \"image\":\""+image+"\",\n          \"description\":\""+desc+"\"\n     }],"
				print(constract)
				close= browser.find_element_by_css_selector(".light > div:nth-child(1) > button:nth-child(1)")
				close.click()
				time.sleep(2)
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(20)

	results.append(constract[:-1])



def main():

	file_handler("read")
	for i in channels_pool:
		#general(i.split("*")[0],i.strip('\n').split("*")[1])
		osn(i.split("*")[0],i.strip('\n').split("*")[1])
	file_handler("write")
	

main()
browser.close()
