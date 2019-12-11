import requests
from bs4 import BeautifulSoup
import itertools
import os


arr=['January','February','March','April','May','June','July','August','September','October','November','December']

def createFile(file_name,r):
	print("Downloading:- "+file_name)
	with open(file_name, 'wb') as x:
		for chunk in r.iter_content(chunk_size=2048*2048):
			if chunk:
				x.write(chunk)

def getComicList(year,month,authors):

	URL="http://explosm.net/comics/archive/"+(str)(year)+"/"+(str)(month)

	r=requests.get(URL)
	Bsoup=BeautifulSoup(r.content,'html5lib')
	table=Bsoup.find('div',attrs={'id' : 'container'})

	lis=[]
	parseLis=[]
	file_names=[]


	for (link, auth) in zip(Bsoup.find_all('div',class_="small-3 medium-3 large-3 columns"), Bsoup.find_all("div",id="comic-author")): 
		#print(link)
		xyz=(str)(link).index("/small-")+7
		abc=((str)(link)).index('.png')
		code=((str)(link))[xyz:abc]
		a=auth.text.split("\n")[1:3]
		if a[1][3:] in authors:
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
			#print(URL2+i+"/")
			#print(r)
			#print(a)
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
		print(i)
		print(i[-4:])
		file_names[0]+=i[-4:]
		createFile(file_names[0],r)
		del file_names[0]



	   

# for node in Bsoup.find_all('div',class_="small-3 medium-3 large-3 columns"):
# 	code=node.[node.index("small-")+6:node.index(".png")]
# 	print(node)
# 	lis.append(code)


# for node in Bsoup.find_all("div",id="comic-author"):
# 	print(node)
# 	a=node.text.split("\n")[1:3]
# 	if a[1][4:] in authors:
# 		parseLis.append[lis[]]




if __name__ == "__main__":

	print("hello".find("!"))
	start_year=2019
	end_year=2019
	start_month=12
	end_month=12
	x=(start_year-2000)*12+start_month
	y=(end_year-2000)*12+end_month
	authors=["Matt Melvin","Kris Wilson"]

	lis=[]


	cwd=os.getcwd()

	for i in range(x,y+1):
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
		getComicList(year,month,authors)
	print(lis)





