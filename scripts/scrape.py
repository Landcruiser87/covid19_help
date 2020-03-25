# #%% 
# from bs4 import BeautifulSoup
# import requests
# import pprint

# URL = 'http://www.us-funerals.com/funeral-homes/#.Xnf9OohKibh'

# page = requests.get(URL)
# soup = BeautifulSoup(page.content, 'html.parser')

# results = soup.find(id='HomeBody')
# print(results.prettify())

#%%

# importing libraries
from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
url="http://www.us-funerals.com/funeral-homes"
page = urllib.request.urlopen(url) # conntect to website
try:
	page = urllib.request.urlopen(url)
except:
	print("An error occured.")
	
soup = BeautifulSoup(page, 'html.parser')
#match=soup.find('div',class_='content-body')
#regex = re.compile('.*state.*')
#content_lis = soup.find_all('li', attrs={'class': regex})
#print(match)

names = []
address = []
badlinks = []
for link in soup.findAll('a',attrs={'href': re.compile(".*state.*")} ):
	url_state = link['href']  
	page = urllib.request.urlopen(url_state)
	soup_state = BeautifulSoup(page, 'html.parser')
	try:
		for link in soup_state.findAll('a',attrs={'href': re.compile(".*city.*")}):
			url_city = link['href']  
			page = urllib.request.urlopen(url_city)
			soup_city = BeautifulSoup(page, 'html.parser')
			try:
				for link in soup_city.findAll('a',attrs={'href': re.compile(".*city.*")}):
			#     print(link['href'])
					url_funeral_home = link['href']  
					page = urllib.request.urlopen(url_funeral_home)
					soup_funeral_home=BeautifulSoup(page, 'html.parser')
					names.append(soup_funeral_home.find('h1').text)
					address.append(soup_funeral_home.find('p').text)
			except:
				badlinks.append(link)
				print("problem with :" , url_funeral_home)
				continue
	except:
		badlinks.append(link)
		print("problem with :" , url_city)
		continue
		



# %%

#%%

filename = "death1.csv"

with open(filename, 'w') as f:
     writer = csv.writer(f, delimiter=',')
     writer.writerows(comb_list)
