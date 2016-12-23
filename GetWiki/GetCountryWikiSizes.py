#collecting the size of the wikipedia articles of countries, saving them in excel and saving down the actual article in plain text

#DOES NOT WORK FOR FRANCE - TO BE DONE MANUALLY

import os, requests, bs4, re, openpyxl

#BeautifulSoup gettext function gives text in a messy format, full of special characters. This function is to clean the text.
def cleanText(sourceText):
    t=str(sourceText.encode('utf-8'))
    t=t[2:-1] #remove b and '' characters
    t=re.sub(r"\\n","-", t) #remove \n (new lines) after the conversion
    t=re.sub(r"\\x..","-", t) #remove spec characters after the conversion
    t=re.sub(r"\\'","\'", t) #remove \ characters in front of 's
    t=re.sub(r"---References.*","",t) #remove text that's not part of the article
    t=re.sub(r".*t TLD","",t,count=1) #remove noise from the first part
    return t

wikiLinks={} #initialise dictionary that will store links to country wiki pages

wikiMain = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)')

mainSoup=bs4.BeautifulSoup(wikiMain.text,"html.parser")

rows=mainSoup.find_all('tr') #find all rows of the table

i=0 #initialise row counter
key=0

print("Starting now...\n")

for row in rows:
    i+=1 #increment row counter
    if i<3:
        continue #skip header and first row (world population)
    
    cells=row.find_all('td') #find all cells
    j=0 #reset cell counter
    
    for cell in cells:
        j+=1
        print("row no: "+str(i)+", cell no: "+str(j)+", text: "+cell.text)
        
        if j==1:
            key=int(cell.text) #1st cell is the population rank of the country
        elif j==2:
            link='https://en.wikipedia.org'+cell.find_all('a')[0].get('href') #get link from the 2nd cell
            wikiLinks[int(key)]=link #add country rank and link to the dictionary
        else:
            break

    if i>234:
        break

print("Links collected:\n")
print(wikiLinks)

print("Opening excel file...\n")
wb=openpyxl.load_workbook(filename="Countries Wiki Size.xlsx")#it already exists, copied the list of countries from wikipedia - only the article sizes have to be added
ws=wb.active
print("Excel open\n")

print("Starting text collection and writing into excel...\n")
ws['h1']="Wiki size" #first unused column in the excel

for k in range(1,len(wikiLinks)+1):
    wikiCountry=requests.get(wikiLinks[k]) #get the article
    wikiCountrySoup=bs4.BeautifulSoup(wikiCountry.text,"html.parser")
    wikiCountryText=wikiCountrySoup.get_text() #get the text from the article
    wikiCountryTextClean=cleanText(wikiCountryText) #remove rubbish left after using get_text
    print("Length of "+str(k)+": "+str(len(wikiCountryTextClean)))
    ws['h'+str(k+1)]=len(wikiCountryTextClean) #data goes to column H

    countryName=wikiLinks[k][30:] #getting the name of the country from the link
    f=open(str(k)+' '+countryName+'.txt','w') #save the text of the article into a plain text file
    f.write(wikiCountryTextClean)
    f.close()

print("Done, closing and saving.\n")
wb.save("Countries Wiki Size.xlsx")
print("All done, bye for now.")
