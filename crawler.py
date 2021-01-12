##########################################
#
#	usando MariaDB ->
#
#  CREATE DATABASE feed
#
#  CREATE TABLE g1tec (
#  title VARCHAR(200),
#  description TEXT(20000),
#  pubdate VARCHAR(100));
#
#  TODO: colocar a data no formato DATE
#		 adicionar validações
#		 deixar o script dinamico para
#         diferentes urls
#
#	
##########################################


import urllib.request
from bs4 import BeautifulSoup
import mariadb
import sys 

# Instantiate Connection
try:
   conn = mariadb.connect(
      user="root",
      password="pronobis",
      host="localhost",
      port=3306,
      database="feed")
except mariadb.Error as e:
   print(f"Error connecting to MariaDB Platform: {e}")
   sys.exit(1)

# Get Cursor 
cur = conn.cursor()

# Deveria ser parametro de entrada:
url = 'https://g1.globo.com/rss/g1/tecnologia/'

req = urllib.request.Request(url)
#inserir validação

with urllib.request.urlopen(req) as response:
   html = response.read()

soup = BeautifulSoup(html, "html.parser")

#find_all retorna uma lista
item = soup.find_all('item')


count = 0
for i in item:
	count=count+1
	print('\n Item {:d} \n'.format(count))
	print(i.find('title').get_text())
	title = i.find('title').get_text()
	description = i.find('description').get_text()
	pubdate = i.find('pubdate').get_text()
	cur.execute(
		"INSERT INTO g1tec (title,description,pubdate) VALUES (?, ?, ?)", 
		(title, description, pubdate))


conn.commit()
conn.close()
