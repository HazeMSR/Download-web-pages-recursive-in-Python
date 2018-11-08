import re
def isHashtag(url):
	p = re.compile('^#{1}')
	return p.match(url)

def isSlash(url):
	p = re.compile('^[\/]{1}')
	return p.match(url)	

def isUnderscore(url):
	p = re.compile('_')
	return p.match(url[-1:])

def hasQuestion(url):
	p = re.compile('[?]+')
	return p.match(url)	

def isWebPage(url):
	p = re.compile('([\.]{1}\w{5}|\w{4}|\w{3}|\w{2}|\w{1})$')
	if p.match(url) != None:
		p2 = re.compile('(([h]{1}[t]{1}[m]{1}[l]{1})|([c]{1}[o]{1}[m]{1})|([o]{1}[r]{1}[g]{1})|([m]{1}[x]{1})|([e]{1}[s]{1})|([e]{1}[n]{1})|([l]{1}[a]{1})|([u]{1}[s]{1})|([i]{1}[o]{1})|([c]{1}[o]{1})|([n]{1}[e]{1}[t]{1})|([a]{1}[s]{1}[p]{1}[x]{1})|([p]{1}[h]{1}[p]{1})|([j]{1}[s]{1}[p]{1}))$')
		if p2.match(url) != None:
			return True
		else:
			return False
	else:
		return True

def isHTML(url):
	p = re.compile('([h]{1}[t]{1}[m]{1}[l]{1})$')
	return p.match(url)

def getName(url):
	r=re.sub('^([h]{1}[t]{2}[p]{1}[s]*[:]{1}[\/]{2})|([\/]+)|([?]+)|$','_',url)
	if isWebPage(r) and isHTML(r) == None:
		return r+".html"
	else:	
		if isUnderscore(r) != None:
			return r[:-1]
		else:			
			return r	

def savePage(name,h):
	f = open(name, 'w',encoding='utf-8')
	f.write(h)
	f.close()

import urllib.request,requests
def saveFile(url,n):
	u = ''
	sleepT=5
	while u == '':
		try:
			u = urllib.request.urlopen(re.sub('[h]{1}[t]{2}[p]{1}[s]{1}','http',url))
			break
		except KeyboardInterrupt:
			print('Someone closed the program')
			raise SystemExit
		except:
			print('Connection refused by the server..')
			print('Sleep for '+str(sleepT)+' seconds')
			print('ZZzzzz...')
			time.sleep(sleepT)
			print('It was a nice sleep, let me continue...')
			sleepT+=1
			continue
	
	f = open(n, 'wb')

	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break	
	    f.write(buffer)	
	f.close()

import time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from pathlib import Path
def getHTML(url,anterior):
	try:
		print(url)
		url=re.sub('[h]{1}[t]{2}[p]{1}[s]{1}','http',url)
	
		resp = ''
		sleepT=5
		while resp == '':
			try:
				resp = requests.get(url)
				break
			except KeyboardInterrupt:
				print('Someone closed the program')
				raise SystemExit
			except:
				print('Connection refused by the server..')
				print('Sleep for '+str(sleepT)+' seconds')
				print('ZZzzzz...')
				time.sleep(sleepT)
				print('It was a nice sleep, let me continue...')
				sleepT+=1
				continue
		
		
		urls = []
		name = getName(url)
		soup = BeautifulSoup(resp.text, 'lxml')	
		a = len(anterior)

		for l in soup.find_all():
			if l.has_attr('href'):
				r=l.attrs['href']
				n=getName(r)
				if isWebPage(r) != None:
					urls.append(r)
				else:
					saveFile(r,n)
				l.attrs['href']=n

			if l.has_attr('src'):
				r=l.attrs['src']
				if hasQuestion(r) != None:
					n=getName(r.split('?')[0])
				else:
					n=getName(r)
				saveFile(r,n)
				l.attrs['src']=n
		savePage(name,str(soup))

		for l in urls:
			if isHashtag(l) == None:
				ur=re.sub('([\/]{1})$','',l)
				if isSlash(l) == None:	
					n=getName(l)
					if a > 0 :
						resta=re.sub(anterior[:-5],'',n)
						c=n[a-5:]
						if c != resta:
							repeti2 = Path(n)
							if not repeti2.is_file():
								getHTML(l,name)	
					else:
						repeti2 = Path(n)
						if not repeti2.is_file():
							getHTML(l,name)
				else:
					n=getName(ur+l)
					if a > 0 :
						resta=re.sub(anterior[:-5],'',n)
						c=n[a-5:]
						if c != resta:
							repeti2 = Path(n)
							if not repeti2.is_file():
								getHTML(ur+l,name)
					else:
						repeti2 = Path(n)						
						if not repeti2.is_file():	
							getHTML(ur+l,name)




	except KeyboardInterrupt:
		print('Someone closed the program')
		raise SystemExit
	
import sys
if __name__ == '__main__':
	url = str(sys.argv[1])
	getHTML(url,'')


#url = 'http://www.example.com'