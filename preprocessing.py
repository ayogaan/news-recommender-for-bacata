from bs4 import BeautifulSoup
import requests
from lxml import html
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

factory = StemmerFactory()
stemmer = factory.create_stemmer()
symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"
stopw = open("stopword.txt", "r")
listofword = []
for line in stopw:
    stripped_line = line.strip()
    line_list = stripped_line.split()
    listofword.append(line_list)
stopw.close()

def splitter(inform, label):
    inform = inform.lower()
    wordlist = inform.split()
    
    
    for word in wordlist:
        for k in listofword[:]:
            try:
                wordlist.remove(k)
                print(k)
            except:
                print("")
    #print(wordlist)
    final_text = label+" "+ stemmer.stem(' '.join(wordlist)+"\n")
    #print(final_text)

def removal(inform, label):
    

    symbol = r'[0-9]'
    for i in symbols:
         inform = inform.replace(i, ' ')
    inform = re.sub(symbol, '', inform)
    
    inform = " "+inform.lower()+" "
    #print(inform)
    #print(inform)
    for i in listofword:
        inform = inform.replace(' '+i[0]+' ', ' ')
        

    inform = inform.replace("  ", ' ')
 
    q = label +" "+ stemmer.stem(inform)
    print(q)

def getText(URL):
    page = requests.get(URL)

    soup = BeautifulSoup(page.content,'html.parser')
    also_read = soup.find_all('div', attrs={'class': 'baca-juga'})

    for tag in also_read:
        tag.decompose()

    em = soup.find_all('em')
    for tag in em:
        tag.decompose()


    content = ""
    cars = soup.find_all('div', attrs={'class': 'article-content-body__item-content'})
    for tag in cars:
        content += tag.text.strip()

    breadcrumb = soup.find_all('li', attrs={'class': 'read-page--breadcrumb--item'})
    
    label = breadcrumb[len(breadcrumb)-1].text.strip()
    #splitter(content, label)
    #print(content+"\n")
    removal(content, label)

urilist = open("urilist.txt", "r")
for line in urilist:
    getText(line)
urilist.close()

