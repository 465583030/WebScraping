#Save the names and prices of the 100 largest cryptocurrencies from coinmarketcap.com

import os, requests, bs4

#getting the list of cryptocurrencies and converting the page into a bs object
cbase = requests.get('https://coinmarketcap.com/all/views/all/')
coinSoup=bs4.BeautifulSoup(cbase.text,"html.parser")

#finding all the rows of the table
ps=coinSoup.find_all('tr')

#open the file in which the data will be stored
f=open("crypto.txt","w")

#for the 100 largest CCs: find the name and the price save them in a new line of the file
for i in range(1,101):
    f.write(str(i)+",")
    f.write(ps[i].find('a').text+",")
    f.write(ps[i].find('a', class_='price').text[1:]+"\n")

#close&save    
f.close()
