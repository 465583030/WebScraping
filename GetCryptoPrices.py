#Save the names and prices of the 100 largest cryptocurrencies from coinmarketcap.com in an excel file

import os, requests, bs4, datetime
from openpyxl import *

#getting the list of cryptocurrencies and converting the page into a bs object
cbase = requests.get('https://coinmarketcap.com/all/views/all/')
coinSoup=bs4.BeautifulSoup(cbase.text,"html.parser")

#finding all the rows of the table
ps=coinSoup.find_all('tr')

#if the excel file does not exist, we create it
if os.path.isfile("cryptoprices.xlsx")==False:
    wb=Workbook()
    wb.save("cryptoprices.xlsx")

#loading the excel file
wb=load_workbook(filename="cryptoprices.xlsx")
ws=wb.active

tday=datetime.date.today()

#for the 100 largest CCs: find the name and the price save them in a new line of the excel file along with today's date
for i in range(1,101):
    ws.append([tday,str(i),ps[i].find('a').text,ps[i].find('a', class_='price').text[1:]])

wb.save("cryptoprices.xlsx")

