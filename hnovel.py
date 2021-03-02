#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    Author:  AmbitionlessFr1end 
    Github: https://github.com/AmbitionlessFr1end/
    Project: h-manga-downloader
    All rights reserved for this awful looking code! :P
    Version: 1.0.3
'''

# Libraries
import time
import sys
import os
import requests
import os
import concurrent.futures
import re
import urllib3
from rich.console import Console
from bs4 import BeautifulSoup

#Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-GB,en;q=0.9',
}

# Saving to folder
def saving(link, path, typeof):
    img_bytes = requests.get(link).content
    with open(path + typeof, 'wb') as img_file:
        img_file.write(img_bytes)

# Initialize Selenium
def init_selen(chromedriver):
    chrome_options = Options()
    chrome_options.add_argument("-headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(chromedriver, options=chrome_options)
    return driver

# Initialize Selenium with no proxy
def init_selen_with_no_proxy(chromedriver):
    chrome_options = Options()
    chrome_options.add_argument("--no-proxy-server")
    chrome_options.add_argument("-headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(chromedriver, options=chrome_options)
    return driver

# Link Checker for Selenium stuff...
def checking_link(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def main():
    console = Console()
    console.print("H","Novel","Seeker", style = "bold blue", justify='center', highlight=True)
    link = sys.argv[1]
    nhbool = False
    h2rbool = False
    purbool = False
    ehentbool = False
    doujins = False
    hentaicafe = False
    tsumino = False
    hbrowse = False
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
    elif link.find('e-hentai') != -1:
        console.log("E-hentai Link Found!")
        ehentbool = True
    elif link.find('doujins') != -1:
        console.log("Doujins Link Found!")
        doujins = True
    elif link.find('hentai.cafe') != -1:
        console.log('Hentai Cafe Link Found!')
        hentaicafe = True
    elif link.find('tsumino') != -1:
        console.log('Tsumino Link Found!')
        tsumino = True
    elif link.find('hbrowse') != -1:
        console.log('HBrowse Link Found!')
        hbrowse = True
    else:
        console.print("Unsupported Link Found",style = 'bold red')
        sys.exit()

    if link[-1:] != '/':
        link = link + '/'

    if nhbool:
        page = requests.get(link + '1')
        # Checking for valid link
        if page.status_code != 200:
            console.print("Invalid link detected. Try again!", style = 'bold red')
            sys.exit()
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
        for i in range(1, numb + 1):
            newlink = link + str(i)
            page = requests.get(newlink)
            soup = BeautifulSoup(page.content, 'html.parser')
            a = soup.find('section', {'id': 'image-container'})
            b = a.find('a')
            c = b.find('img')['src']
            d = c[-4:]
            path = newpath + str(i)
            with console.status("[bold green]Scraping data...") as status:
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                        executor.submit(saving, c, path, d)
                        console.log(f"[green]Scraping data[/green] {'Image ' + str(i) + ' fetched'}")
        console.log(f'[bold][red]Done!')
        end = time.time()
        print (end - start)
    elif h2rbool:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        a = soup.find('ol', {'class': 'breadcrumb'})
        # Checking for valid link       
        if a is None:
            console.print("Invalid link detected. Try again!", style = 'bold red')
            sys.exit()
        b = a.findAll('li')
        title = b[2].find('a').text
        title = title.replace('\n', '')
        console.log('Novel Found: ' + title)
        chaptrs = soup.find('ul', {'class': 'nav-chapters'})
        # Checking for valid link       
        if chaptrs is None:
            console.print("Invalid link detected. Try again!", style = 'bold red')
            sys.exit()
        chpttt = chaptrs.findAll('li')
        for item in chpttt:
            div = item.find('div', {'class': 'media'})
            a = div.find('a', {'class': 'pull-left font-w600'}).text
            lst = re.findall(r'\d*\.?\d+', a)
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
        driver = init_selen_with_no_proxy(chromedriver)
        driver.get(link)
        # Checking for valid link
        if (checking_link(driver,"//div[@class='image-holder']/img[@class='img-fluid']")) == False:
            console.print("Invalid link detected. Try again!", style = 'bold red')
            sys.exit()
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
    elif ehentbool:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        page = requests.get(link, headers=headers, verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')
        a = soup.find('div',{'class' : 'gm'})
        # Checking for valid link
        if a is None:
            console.print("Invalid link detected. Try again!", style = 'bold red')
            sys.exit()
        b = a.find('div',{'id' : 'gd2'})
        title = b.find('h1').text
        console.log('Novel Found: ' + title)
        gdt = soup.find('div',{'id' : 'gdt'})
        gdtm = gdt.find('div',{'class' : 'gdtm'})
        next1 = gdtm.find('div')
        newlink = next1.find('a')['href']
        page = requests.get(newlink, headers=headers, verify=False)
        soup = BeautifulSoup(page.content,'html.parser')
        curpath = sys.path[0]
        start = time.time()
        newpath = curpath + '/hnovels' + '/E-Hentai' + '/' + title + '/'
        numb = 1
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        while(True):
            f = soup.find('div',{'id' : 'i3'})
            a = f.find('a')
            img = a.find('img', {'id' : 'img'})['src']
            old = page.url
            nextlin = a['href']
            if old == nextlin:
                break
            typeof = img[-4:]
            with console.status("[bold green]Scraping data...") as status:
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                        path = newpath + '/' + str(numb)
                        executor.submit(saving, img, path, typeof)
                        console.log(f"[green]Scraping data[/green] {'Image ' + str(numb) + ' fetched'}")
            page = requests.get(nextlin, headers=headers, verify=False)
            soup = BeautifulSoup(page.content, 'html.parser')
            numb +=1
        end = time.time()
        console.log(f'[bold][red]Done!')
        print (end - start)
    elif doujins:
        chromedriver = './chromedriver'
        driver = init_selen(chromedriver)
        driver.get(link)
        if (checking_link(driver,"//div[@class='folder-title']/a[@href='#']")) == False:
            console.print("Invalid link detected. Try again!", style = 'bold red')
            sys.exit()
        title = driver.find_element_by_xpath("//div[@class='folder-title']/a[@href='#']").text
        console.log('Novel Found: ' + title)
        a = driver.find_elements_by_xpath('//div[@class="col-12"]/div[@id="gallery"]/div[@id="thumbnails"]/div[@class="thumbnails"]/div[@class="col-6 col-sm-4 col-md-3 col-lg-2 px-1"]')
        b = a[0].find_element_by_xpath("//div[@class='thumbnail-doujin']/a").get_attribute('href')
        driver.get(b)
        curpath = sys.path[0]
        start = time.time()
        newpath = curpath + '/hnovels' + '/Doujins' + '/' + title + '/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        c = driver.find_elements_by_xpath("//div[@id='gallery']/div[@id='images']/div")
        d = c[0].find_elements_by_xpath("//div[@class='col-12 text-center']/div[@id='controllers']/div[@class='btn-group']")
        e = d[0].find_element_by_xpath("//span[@id='image-counter']").text
        pages = e[-4:].replace('/ ','')
        pages = int(pages) + 1
        for i in range(1,pages):
            c = driver.find_elements_by_xpath("//div[@id='gallery']/div[@id='images']/div")
            imgs = c[1].find_elements_by_xpath("//div[@id='image-container']/img[@id='doujinScroll']")
            img = imgs[i-1].get_attribute('src')
            typeof = img[37:41]   
            with console.status("[bold green]Scraping data...") as status:
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                        path = newpath + '/' + str(i)
                        executor.submit(saving, img, path, typeof)
                        console.log(f"[green]Scraping data[/green] {'Image ' + str(i) + ' fetched'}")
            e = c[0].find_elements_by_xpath("//div[@class='col-12 text-center']/div[@id='controllers']/div[@class='btn-group']")
            next1 =  e[0].find_element_by_xpath("//a[@class='btn btn-transparent image-next']").get_attribute('href')
            driver.get(next1)
        end = time.time()
        console.log(f'[bold][red]Done!')
        print (end - start) 
        driver.close()
    elif hentaicafe:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        a = soup.find('div', {'class' : 'x-column x-sm x-1-2 last'})
        if a is None:
            console.print("Invalid link detected. Try again!", style = 'bold red')
            sys.exit()
        title = a.find('h3').text
        console.log('Novel Found: ' + title)
        c = soup.find('a', {'class' : 'x-btn x-btn-flat x-btn-rounded x-btn-large'})['href']
        page = requests.get(c)
        soup = BeautifulSoup(page.content, 'html.parser')
        b = soup.find('div', {'class' : 'tbtitle dropdown_parent dropdown_right mmh'})
        count = b.find('div').text
        count = count[:-1]
        count = int(count.replace(' ', ''))
        curpath = sys.path[0]
        newpath = curpath + '/hnovels' + '/HentaiCafe' + '/' + title + '/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        start = time.time()
        for i in range(1, count + 1):
            src = soup.find('img', {'class' : 'open'})['src']
            typeof = src[-4:]
            with console.status("[bold green]Scraping data...") as status:
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                        path = newpath + '/' + str(i)
                        executor.submit(saving, src, path, typeof)
                        console.log(f"[green]Scraping data[/green] {'Image ' + str(i) + ' fetched'}")
            dd = soup.find('div',{'class': 'inner'})
            nextl = dd.find('a')['href']
            page = requests.get(nextl)
            soup = BeautifulSoup(page.content, 'html.parser')
        end = time.time()
        console.log(f'[bold][red]Done!')
        print (end - start) 
    elif tsumino:
        if link.find('videos') != -1  or link.find('books') != -1:
            console.print("Invalid link detected. Try again!", style = 'bold red')
            sys.exit()
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        if soup.find('video'): 
            console.print("Invalid file format. Try again!", style = 'bold red')
            sys.exit()
        numbs = re.search(r'\d+$', link.replace('/',''))
        if link[-7:].find('page') != -1:
            first = link
        elif numbs:
            entry_id = (numbs.group())
            first = 'https://www.tsumino.com/' + 'Read/Index/' + entry_id + '?page=1' 
        else:
            console.print("Invalid link detected. Try again!", style = 'bold red')
            sys.exit()
        chromedriver = './chromedriver'
        driver = init_selen(chromedriver)
        driver.get(first)
        cururl = driver.current_url
        if (cururl.find('AUTH') != -1):
            console.print("Captcha in website. Authenticate and try again!", style = 'bold red')
            sys.exit()
        b = driver.find_element_by_xpath("//div[@id='rootContainer']/div[@class='row row-no-margin center-block reader-btn']")
        b = driver.find_element_by_xpath('//div[@class="row row-no-margin center-block reader-btn"]/div[@class="col-md-12 col-no-padding"]/h1').text
        pages = b[-4:].replace('f ','')
        pages = int(pages)
        title = driver.title
        title = title.split('/',1)
        title = title[0].replace('Tsumino | Read ','')
        imgcontain = driver.find_element_by_xpath('//div[@id="image-container"]').get_attribute('data-cdn')
        driver.close()
        typeof = '.jpeg'
        curpath = sys.path[0] 
        newpath = curpath + '/hnovels' + '/Tsumino' + '/' + title + '/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        start = time.time()
        for i in range(1, pages + 1):
            src = imgcontain.replace('[PAGE]', str(i))
            with console.status("[bold green]Scraping data...") as status:
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    path = newpath + '/' + str(i)
                    executor.submit(saving, src, path, typeof)
                    console.log(f"[green]Scraping data[/green] {'Image ' + str(i) + ' fetched'}")
        end = time.time()
        console.log(f'[bold][red]Done!')
        print (end - start)  
    elif hbrowse:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        a = soup.findAll('td', {'class' : 'listMiddle'})
        if len(a) > 1:
            for item in a:
                href = item.find('a')['href']
                chptitle = item.find('a').text
                chptitle = chptitle.replace('View ', '')
                newlink = 'http://hbrowse.com' + href
                page = requests.get(link)
                soup = BeautifulSoup(page.content, 'html.parser')
                img = soup.find('img')['src']
                if img.find('lockedManga') != -1:
                    console.print("Locked manga detected. Try again!", style = 'bold red')
                    sys.exit()
                span = soup.find('span', { 'id' : 'jsPageList'})
                dd = span.findAll('a')
                pages = dd[-1].text
                pages = int(pages)
                typeof = img[-4:]
                title = soup.find('td', {'class' : 'listLong'}).text
                curpath = sys.path[0] 
                newpath = curpath + '/hnovels' + '/HBrowse' + '/' + title + '/' + chptitle + '/'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                start = time.time()
                for i in range(1, pages + 1):
                    src = 'http://www.hbrowse.com' + img
                    with console.status("[bold green]Scraping data...") as status:
                        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                            path = newpath + '/' + str(i)
                            executor.submit(saving, src, path, typeof)
                            console.log(f"[green]Scraping data[/green] {'Image ' + str(i) + ' fetched'}")
                        next1 = soup.find('a', {'name' : 'next'})['href']
                        newlink = 'http://www.hbrowse.com' + next1
                        page = requests.get(newlink)
                        soup = BeautifulSoup(page.content, 'html.parser')
                        img = soup.find('img')['src']
                end = time.time()
                console.log(f'[bold][red]Done!')
                print (end - start)
            sys.exit()
        img = soup.find('img')['src']
        if img.find('lockedManga') != -1:
            console.print("Locked manga detected. Try again!", style = 'bold red')
            sys.exit()
        span = soup.find('span', { 'id' : 'jsPageList'})
        dd = span.findAll('a')
        pages = dd[-1].text
        pages = int(pages)
        typeof = img[-4:]
        title = soup.find('td', {'class' : 'listLong'}).text
        curpath = sys.path[0] 
        newpath = curpath + '/hnovels' + '/HBrowse' + '/' + title + '/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        start = time.time()
        for i in range(1, pages + 1):
            src = 'http://www.hbrowse.com' + img
            with console.status("[bold green]Scraping data...") as status:
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    path = newpath + '/' + str(i)
                    executor.submit(saving, src, path, typeof)
                    console.log(f"[green]Scraping data[/green] {'Image ' + str(i) + ' fetched'}")
                next1 = soup.find('a', {'name' : 'next'})['href']
                newlink = 'http://www.hbrowse.com' + next1
                page = requests.get(newlink)
                soup = BeautifulSoup(page.content, 'html.parser')
                img = soup.find('img')['src']
        end = time.time()
        console.log(f'[bold][red]Done!')
        print (end - start) 

if __name__ == "__main__":
    main()      
    