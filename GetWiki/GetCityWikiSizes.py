#collecting the size of the wikipedia articles of cities, saving them in excel and saving down the actual article in plain text

import os, requests, bs4, re, openpyxl

#BeautifulSoup gettext function gives text in a messy format, full of special characters. This function is to clean the text.
def cleanText(sourceText):

    t=str(sourceText.encode('utf-8'))
    
    t=t[2:-1] #remove b and '' characters
    t=re.sub(r"\\n","-", t) #remove \n (new lines) after the conversion
    t=re.sub(r"\\x..","-", t) #remove spec characters after the conversion
    t=re.sub(r"\\'","\'", t) #remove \ characters in front of 's
    t=re.sub(r"--References.*","",t) #remove text that's not part of the article
    t=re.sub(r".*From Wikipedia, the free encyclopedia","",t,count=1) #remove noise from the first part
    return t

wikiLinks={} #initialise dictionary that will store the links to city wiki pages

wikiMain = requests.get('https://en.wikipedia.org/wiki/List_of_cities_proper_by_population')

mainSoup=bs4.BeautifulSoup(wikiMain.text,"html.parser")

rows=mainSoup.find_all('tr') #find all rows of the table

i=0 #initialise row counter
key=0

print("Starting now...\n")

for row in rows:
    i+=1 #increment row counter
    if i<6:
        continue #skip first table on page and header
    
    cells=row.find_all('td') #find all cells
    j=0 #reset cell counter
    
    for cell in cells:
        j+=1
        print("row no: "+str(i)+", cell no: "+str(j)+", text: "+cell.text)
        
        if j==1:
            key=int(cell.text) #1st cell is the population rank of the city
        elif j==2:
            link='https://en.wikipedia.org'+cell.find_all('a')[0].get('href') #get link from the 2nd cell
            wikiLinks[int(key)]=link #add city rank and link to the dictionary
        else:
            break

    if i>96:
        break

print("Links collected:\n")
print(wikiLinks)

print("Opening excel file...\n")
wb=openpyxl.load_workbook(filename="Cities Wiki Size.xlsx")#it already exists, copied the list of cities from wikipedia - only the article sizes have to be added
ws=wb.active
print("Excel open\n")

print("Starting text collection and writing into excel...\n")
ws['h1']="Wiki size" #first unused column in the excel

for k in range(1,len(wikiLinks)+1):
    wikicity=requests.get(wikiLinks[k]) #get the article
    wikicitySoup=bs4.BeautifulSoup(wikicity.text,"html.parser")
    wikicityText=wikicitySoup.get_text() #get the text from the article
    wikicityTextClean=cleanText(wikicityText) #remove rubbish left after using get_text
    print("Length of "+str(k)+": "+str(len(wikicityTextClean)))
    ws['h'+str(k+1)]=len(wikicityTextClean) #data goes to column H

    cityName=wikiLinks[k][30:] #getting the name of the city from the link
    f=open(str(k)+' '+cityName+'.txt','w') #save the text of the article into a plain text file
    f.write(wikicityTextClean)
    f.close()

print("Done, closing and saving.\n")
wb.save("Cities Wiki Size.xlsx")
print("All done, bye for now.")
