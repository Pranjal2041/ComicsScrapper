import requests
from bs4 import BeautifulSoup
import itertools
import os
from datetime import datetime
import sys


arr=['January','February','March','April','May','June','July','August','September','October','November','December']

def createFile(file_name,r):    #Creates a file
	print("Downloading:- "+file_name)
	with open(file_name, 'wb') as x:
		for chunk in r.iter_content(chunk_size=2048*2048):
			if chunk:
				x.write(chunk)

def getComicList(year,month,authors,max_files):

	URL="http://explosm.net/comics/archive/"+(str)(year)+"/"+(str)(month)

	r=requests.get(URL)
	Bsoup=BeautifulSoup(r.content,'html5lib')

	lis=[]
	parseLis=[]
	file_names=[]


	for (link, auth) in zip(Bsoup.find_all('div',class_="small-3 medium-3 large-3 columns"), Bsoup.find_all("div",id="comic-author")): 
		if(max_files<=0):
			break
		max_files-=1
		xyz=(str)(link).index("/small-")+7
		abc=((str)(link)).index('.png')
		code=((str)(link))[xyz:abc]
		a=auth.text.split("\n")[1:3]
		if((authors==[])or(a[1][3:] in authors)):
			parseLis.append(code)
			file_names.append(a[0]+"-"+a[1][3:])
		

	URL2="http://explosm.net/comics/"

	img=[]
	count=0
	for i in parseLis:
		r=requests.get(URL2+i+"/")
		Bsoup=BeautifulSoup(r.content,'html5lib')
		try:
			a=(str)(Bsoup.find("img",id="main-comic"))
			abc=(int)(a.index("src=")+5)
			xyz=(int)(a.index("/>")-1)
			a=a[abc:xyz]
			img.append("http:"+a)
		except:
			if(i==""):
				parseLis.append("5108")
				continue
			print("Unable to download file:-   "+file_names[count])
		count+=1


	for i in img:
		if(i.find('?')!=-1):
			i=i[:i.index('?')]
		r=requests.get(i,stream=True)
		file_names[0]+=i[-4:]
		createFile(file_names[0],r)
		del file_names[0]

	return max_files



if __name__ == "__main__":

	todayMonth = datetime.now().month
	todayYear = datetime.now().year
	authors=[]
	query="random"
	cwd=os.getcwd()
	sm=""
	em=""
	start_year=2005
	end_year=todayYear

	try:
		file=open("input.txt","r")
		res=(file.read())
		res=res.split("\n")
		for i in res:
			if i[0]=="#":
				continue
			if i.lower()=="Random".lower():
				query="random"
			elif i[:i.find(' ')].lower()=='latest'.lower():
				query="latest"
				x=(int)(i[i.find(' ')+1:])
			else:
				query="dateRange"
				if ((sm)and(not(em))):
					em=i[:i.find(' ')]
					end_year=(int)((i[i.find(' ')+1:]))
				elif(not(em)):
					sm=i[:i.find(' ')]
					start_year=(int)((i[i.find(' ')+1:]))
				else:
					auth=i.split(",")
					for j in auth:
						authors.append(j.strip()) 
			
	except Exception as e:
		print("Error reading file"+e)


				



	max_files=9999  # An arbitary large number


	if(query=="latest"):
		max_files=x
		end_year=todayYear
		end_month=todayMonth
		start_month=1
		start_year=2005
	elif(query=="random"):
		URL="http://explosm.net/rcg"
		r=requests.get(URL)
		Bsoup=BeautifulSoup(r.content,'html5lib')
		a=(str)(Bsoup.find('div',class_="rcg-panels"))		
		a=a.split("src=\"")
		rnd_path=os.path.join(cwd,"random")
		if(not(os.path.exists(rnd_path))):
				os.mkdir(rnd_path)
		os.chdir(rnd_path)
		for i in range(3):
			a[i+1]=a[i+1][:a[i+1].index('"/')]
			r=requests.get(a[i+1],stream=True)
			createFile("frame"+(str)(i+1)+a[i+1][-4:],r)
		sys.exit(0)
	else:
		for i in range(12):
			if(arr[i].lower()==sm.lower()):
				start_month=i+1
			if(arr[i].lower()==em.lower()):
				end_month=i+1

	

	x=(start_year-2000)*12+start_month
	y=(end_year-2000)*12+end_month

	lis=[]


	for i in range(y,x-1,-1):
		year=(int)((i+24000-1)/12)
		month=(int)((i-1)%12+1)
		year_path=os.path.join(cwd,(str)(year))
		if(not(os.path.exists(year_path))):
			os.mkdir(year_path)
		os.chdir(year_path)

		month_path=os.path.join(year_path,arr[month-1])
		if(not(os.path.exists(month_path))):
			os.mkdir(month_path)
		os.chdir(month_path)
		max_files=getComicList(year,month,authors,max_files)
		if(max_files==0):
			break