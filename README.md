# H Manga/Doujin Downloader


A script that downloads hentai files from websites and stores them in a folder. <br>

### Prerequisites/Installation

The prerequisites needed are:
  
  - **rich** : Text formmating 
    ```bash
      $ pip install rich 
    ```
  - **selenium** : Crawling in the js websites 
    ```bash
      $ pip install selenium
    ```
  - **requests** : Calling website
    ```bash
      $  python -m pip install requests
    ```
  - **BeautifulSoup from bs4** : Parsing requests call for crawling
    ```bash
      $ pip install beautifulsoup4
    ```
  - **concurrent.futures** : Parallel tasks
    ```bash
      $ pip install futures
    ```

### Websites Supported

 - Hentai2Read
 - Pururin
 - Nhentai

### Problems
 - Messy code
 - A bit on the slow side (depends on computer and network)

### Comments

  I know that you can already download from some or all of the websites listed, but they need you to create an account for their websites. <br>
  I'm not a fan of that so voila! <br>
  I don't have any problem with account making, but personally I don't have any use for an account except for downloading files so I created this file as a result!

### Usage 
  ```bash
    $ python hnovel.py link 
  ```
  link is the url of a h manga/doujin from the sites 
