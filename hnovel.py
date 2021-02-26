#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Author:  AmbitionlessFr1end 
    Github: https://github.com/AmbitionlessFr1end/
    Project: h-manga-downloader
    All rights reserved for this awful looking code! :P
'''

# Libraries
import time
import sys
import os
import requests
import urllib
import os
import concurrent.futures
import re
from rich.console import Console
from bs4 import BeautifulSoup

#Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Writing nhentai files to specified folder
def nhentai(link, i, path):
    newlink = link + str(i)
    page = requests.get(newlink)
    soup = BeautifulSoup(page.content, 'html.parser')
    a = soup.find('section', {'id': 'image-container'})
    b = a.find('a')
    c = b.find('img')['src']
    d = c[-4:]
    img_bytes = requests.get(c).content
    with open(path + d, 'wb') as img_file:
        img_file.write(img_bytes)

# Saving to folder
def saving(link, path, typeof):
    img_bytes = requests.get(link).content
    with open(path + typeof, 'wb') as img_file:
        img_file.write(img_bytes)

# Initialize Selenium
def init_selen(chromedriver):
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=chrome-data")
    chrome_options.add_argument("--no-proxy-server")
    # chrome_options.add_argument("--proxy-server='direct://'")
    # chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("-headless")
    driver = webdriver.Chrome(chromedriver, options=chrome_options)
    return driver

def main():
    console = Console()
    console.print("H","Novel","Seeker", style = "bold blue", justify='center', highlight=True)
    link = sys.argv[1]
    nhbool = False
    h2rbool = False
    purbool = False
    h2rchptrlist = []

    if link.find('nhentai') != -1:
        console.log("Nhentai Link Found!")
        nhbool = True
    elif link.find('hentai2read') != -1:
        console.log("Hentai2Read Link Found!")
        h2rbool = True
    elif link.find('pururin') != -1:
        console.log("Pururin Link Found!")
        purbool = True
    else:
        sys.exit()
    if link[-1:] != '/':
        link = link + '/'
    if nhbool:
        page = requests.get(link + '1')
        soup = BeautifulSoup(page.content, 'html.parser')
        btnclass = soup.find('button', {'class': 'page-number btn btn-unstyled'})
        numberofpages = btnclass.find('span', {'class': 'num-pages'}).text
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        titleclass = soup.find('h1', {'class': 'title'})
        spanclass = titleclass.findAll('span')
        title = spanclass[1].text
        console.log('Novel Found: ' + title)
        numb = int(numberofpages)
        curpath = sys.path[0]
        newpath = curpath + '/hnovels' + '/Nhentai' + '/' + title + '/'
        
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        start = time.time()
        with console.status("[bold green]Scraping data...") as status:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as \
                executor:
                for i in range(1, numb):
                    path = newpath + str(i)
                    executor.submit(nhentai, link, i, path)

                    console.log(f"[green]Scraping data[/green] {'Image ' + str(i) + ' fetched'}")

        console.log(f'[bold][red]Done!')
        end = time.time()
        print (end - start)
    elif h2rbool:

        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        a = soup.find('ol', {'class': 'breadcrumb'})
        b = a.findAll('li')
        title = b[2].find('a').text
        title = title.replace('\n', '')
        console.log('Novel Found: ' + title)
        chaptrs = soup.find('ul', {'class': 'nav-chapters'})
        chpttt = chaptrs.findAll('li')
        
        for item in chpttt:
            div = item.find('div', {'class': 'media'})
            a = div.find('a', {'class': 'pull-left font-w600'}).text
            lst = re.findall('\d*\.?\d+', a)
            h2rchptrlist.append(lst[0])
        
        curpath = sys.path[0]
        start = time.time()
        with console.status("[bold green]Scraping data...") as status:
            for item in h2rchptrlist:
                numb = 1
                newpath = curpath + '/hnovels' + '/Hentai2read' + '/' + title + '/' + item + '/'
                
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                
                while True:
                    newlink = link + item + '/' + str(numb)
                    page = requests.get(newlink)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    a = soup.find('div', {'id': 'js-reader'})
                    b = a.find('img', {'id': 'arf-reader'})['src']
                    if numb == 1:
                        typeof = b[-4:]
                    check = b.endswith(typeof)
                    if check != True:
                        break
                    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                        path = newpath + '/' + str(numb)
                        executor.submit(saving, b, path, typeof)

                        console.log(f"[green]Scraping data[/green] {'Image ' + str(numb) + ' fetched'}")
                    numb += 1
        end = time.time()
        console.log(f'[bold][red]Done!')
        print (end - start)
    elif purbool:
        originlink = link
        link = link[:33] + '01/' + link[33:]  
        link = link.replace('gallery','read')
        chromedriver = './chromedriver'
        driver = init_selen(chromedriver)
        driver.get(link)
        src = driver.find_element_by_xpath("//div[@class='image-holder']/img[@class='img-fluid']").get_attribute('src')
        driver.close()
        numb = 1
        typeof = src[-4:]
        subs = src[:-5]
        page = requests.get(originlink)
        soup = BeautifulSoup(page.content,'html.parser')
        divclass = soup.find('div',{"class" : 'title'})
        title = divclass.find('h1').text
        title = title.split('/',1)
        title = title[0]
        console.log('Novel Found: ' + title)
        curpath = sys.path[0]
        start = time.time()
        newpath = curpath + '/hnovels' + '/Pururin' + '/' + title + '/'
        
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        with console.status("[bold green]Scraping data...") as status:
            while True:
                src = subs + str(numb) + typeof
                page = requests.get(src)
                if page.status_code != 200:
                    break
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    path = newpath + '/' + str(numb)
                    executor.submit(saving, src, path, typeof)
                    console.log(f"[green]Scraping data[/green] {'Image ' + str(numb) + ' fetched'}")
                numb +=1
        
        end = time.time()
        console.log(f'[bold][red]Done!')
        print (end - start)


if __name__ == "__main__":
    main()