import bs4
from tkinter import filedialog
import requests
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import shutil
import re
import zipfile

def getMangaPage(link):
    r = requests.get(link)
    if(r.status_code == 200):
        return r.text
    return -1

def createDriver():
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver_options.add_argument("window-size=10000,10000")
    return webdriver.Chrome(options=driver_options)

def downloadChapter(link, folder, driver):
    driver.get(link)
    p = driver.find_element_by_class_name('container-chapter-reader')
    pages = p.find_elements_by_tag_name('img')
    print("Downloading " + folder)
    for page in pages:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", page)
            filePth = folder + "/" + str(pages.index(page))+".png"
            page.screenshot(filePth)
        except Exception as e:
            print("Unable to download Page")
            print(e)
            os.chdir("..")
            shutil.rmtree("cache")
    print("Finished Downloading " + folder)



def zipManga(Savedir, title):
    chapters = os.listdir('.')
    with zipfile.ZipFile(Savedir+"/"+title+".cbz", 'w') as x:
        print("Zipping file")
        for i in chapters:
            pages = os.listdir(i)
            for page in pages:
                x.write(i+"/"+page)

def checkSource(link):
    try:
        r = requests.get(link)
        if r.status_code != 200:
            return False
        if "https://manganelo.com/manga/" in link:
            if ("404 - PAGE NOT FOUND") in r.text: #manganelo returns a 200 response even though the link is not valid
                return False
            return True
        return False
    except Exception as e:
        print(e)
        return False

def main():
    if len(sys.argv) != 2:
        print("Please add a manganelo link")
        sys.exit(-1)
    link = sys.argv[1]
    if checkSource(link) == False:
        print("Please input valid link")
        sys.exit(-1)

    saveFolder = filedialog.askdirectory()
    driver = createDriver()
    cacheDic = "cache"
    if os.path.exists(cacheDic):
        shutil.rmtree(cacheDic)
        os.mkdir(cacheDic)
    else:
        os.mkdir(cacheDic)
    os.chdir(cacheDic)
    try:
        mangaSource = bs4.BeautifulSoup(getMangaPage(link))
        title = mangaSource.find("div", {"class": "story-info-right"}).find("h1").text
        mangaChapters = list(reversed(mangaSource.find("ul", {"class": "row-content-chapter"}).findAll("a")))
        tasks = []

        for i in mangaChapters:
            chapter = re.sub("[.:\/#\\<>$£+%^&*{}:@=|!\"]","",i['title'])
            os.mkdir(chapter)
            downloadChapter(i['href'],chapter,driver)

        zipManga(saveFolder, title)
        os.chdir("..")
        shutil.rmtree(cacheDic)
    except:
        print("Please input a valid manganelo link")
        os.chdir("..")
        shutil.rmtree(cacheDic)
        sys.exit(-1)


if __name__ == "__main__":
    main()
