# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from random import randrange

def LoadUpProxies():
	out = []
	url='https://sslproxies.org/'
	header = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
	}
	response=requests.get(url,headers=header)
	soup=BeautifulSoup(response.content, 'lxml')
	for item in soup.select('#proxylisttable tr'):
		try:
			out.append({'ip': item.select('td')[0].get_text(), 'port': item.select('td')[1].get_text()})
		except:
			print('')

	return out

proxies = LoadUpProxies()
rnd=randrange(len(proxies))
randomIP=proxies[rnd]['ip']
randomPort=proxies[rnd]['port']
print(randomIP)
print(randomPort)
