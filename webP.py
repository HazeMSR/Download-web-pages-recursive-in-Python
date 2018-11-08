
def valida(url):
	p = re.compile('^#{1}')
	return p.match(url)

def valida2(url):
	p = re.compile('^[\/]{1}')
	return p.match(url)	
def isHTML(url):
	p = re.compile('([\.]{1}\w{5}|\w{4}|\w{3}|\w{2}|\w{1})$')
	if p.match(url):
		p2 = re.compile('(([h]{1}[t]{1}[m]{1}[l]{1})|([c]{1}[o]{1}[m]{1})|([o]{1}[r]{1}[g]{1})|([m]{1}[x]{1})|([e]{1}[s]{1})|([e]{1}[n]{1})|([l]{1}[a]{1})|([u]{1}[s]{1})|([i]{1}[o]{1})|([c]{1}[o]{1})|([n]{1}[e]{1}[t]{1})|([a]{1}[s]{1}[p]{1}[x]{1})|([p]{1}[h]{1}[p]{1})|([j]{1}[s]{1}[p]{1}))$')
		if p2.match(url):
			return True
		else:
			return False
	else:
		return True
def getName(url):
	r=re.sub('^([h]{1}[t]{2}[p]{1}[s]*[:]{1}[\/]{2})|([\/]+)|([?]+)|$','_',url)
	if isHTML(r):
		return r+".html"
	else:		
		return r
	


import time
import urllib.request,requests,re
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from pathlib import Path

def guardar(name,h):
	f = open(name, 'w',encoding='utf-8')
	f.write(h)
	f.close()

def getHTML(url,anterior):
	print("anterior")
	print(anterior)
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
				print('Alguien cerro el programa')
				raise SystemExit
			except:
				print('Coneccion rechazada por el servidor..')
				print('Dejame dormir '+str(sleepT)+' segundos')
				print('ZZzzzz...')
				time.sleep(sleepT)
				print('Fue un buen descanso, vamos a continuar...')
				sleepT+=1
				continue
		
		
		urls = []
		name = getName(url)
		
		soup = BeautifulSoup(resp.text, 'lxml')	
		
		hh = soup.find_all('a')
		a = len(anterior)
		for h in hh:
			if h.has_attr('href'):
				r=h.attrs['href']
				print(r)
				#print(valida(r))
				#print(valida2(r))

				if valida(r) == None:
					u=re.sub('[\/]{1}$','',url)
					
					if valida2(r) == None:
						n=getName(r)

						if a > 0 :

							resta=re.sub(anterior[:-5],'',n)
							print("\nresta:")
							print(resta)
							c=n[a-5:]
							print("c:")
							print(c)

							if c != resta:
								print("Entro1")
								repeti2 = Path(n)
								h.attrs['href']=n
								guardar(name,str(soup))

								if not repeti2.is_file():
									#f = open(n, 'w',encoding='utf-8')
									#f.close()
									print("anterior: "+name)
									getHTML(r,name)
								

						else:
							print("Entro2")
							h.attrs['href']=n
							guardar(name,str(soup))
							repeti2 = Path(n)

							if not repeti2.is_file():
								print("anterior: "+name)
								getHTML(r,name)
							h.attrs['href']=n
					else:
						n=getName(u+r)


						if a > 0 :
							resta=re.sub(anterior[:-5],'',n)
							print("\nresta:")
							print(resta)
							c=n[a-5:]
							print("c:")
							print(c)
							if c != resta:
								print("Entro2")
								h.attrs['href']=n
								guardar(name,str(soup))
								repeti2 = Path(n)
				
								if not repeti2.is_file():

									print("anterior: "+name)
									getHTML(u+r,name)
						else:
							h.attrs['href']=n
							guardar(name,str(soup))
							repeti2 = Path(n)
							
							if not repeti2.is_file():
								print("anterior: "+name)
								getHTML(u+r,name)
				#print(h.attrs['href'])



	except KeyboardInterrupt:
		print('Alguien cerro el programa')
		raise SystemExit
	
import sys
if __name__ == '__main__':
	url = str(sys.argv[1])
	getHTML(url,'')

#url = 'http://www.example.com'