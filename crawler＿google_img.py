from selenium import webdriver
import time
import urllib
import os
import requests
from bs4 import BeautifulSoup
import sys


def init_browser(url):
    chrome_driver = '/Users/kuangtinghsiao/python/chromedriver'
    driver = webdriver.Chrome(chrome_driver)
    driver.get(url)
    driver.maximize_window()
    return driver


def download_img(browser, round=5):
    picpath = '/Users/kuangtinghsiao/Pictures/crawler/{}'.format(keyword)
    if not os.path.exists(picpath):
        os.mkdir(picpath)
    url_dic = []

    count = 0
    pos = 0
    for i in range(round):
        #print('This is round {}'.format(round))
        pos += 50
        js = 'var q=document.documentElement.scrollTop=' + str(pos)
        browser.execute_script(js)
        time.sleep(1)

        img_elements = browser.find_elements_by_tag_name('img')
        for img_element in img_elements:
            img_url = img_element.get_attribute('src')
            # print(img_url)
            if isinstance(img_url, str):
                if len(img_url) <= 200:
                    if 'images' in img_url:
                        if img_url not in url_dic:
                            try:
                                url_dic.append(img_url)
                                filename = '{}/{}.jpg'.format(picpath, count)
                                r = requests.get(img_url)
                                with open(filename, 'wb') as f:
                                    f.write(r.content)
                                f.close()
                                count += 1
                                print('This is {} img'.format(count))
                                time.sleep(0.2)
                            except:
                                print('Failure')


if __name__ == '__main__':
    usage = """
    usage python crawler.py {pic you want to crawler}
    """
    if len(sys.argv) == 1:
        print(usage)
    else:
        keyword = sys.argv[1]
        url = 'https://www.google.com.tw/search?q='+keyword+'&tbm=isch'
        browser = init_browser(url)
        download_img(browser)
