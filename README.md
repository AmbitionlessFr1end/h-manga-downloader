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
  - **urllib3** : Fixing ssl certification warning in e-hentai
    ```bash
      $ pip install urllib3
    ```

### Websites Supported

 - Hentai2Read
 - Pururin
 - Nhentai
 - E-hentai

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
  link is the url of a h manga/doujin from the sites <br>
  
  The files will be downloaded to the folder the script is in. For example nhentai files will be downloaded to location/hnovels/Nhentai/, hentai2read to location/novels/Hentai2Read/ etc.
