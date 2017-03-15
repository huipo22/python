# -*- coding:utf-8 -*-

from selenium import webdriver
import time
from bs4 import BeautifulSoup

def getUrl(bsObj):
    # 每页的urls
    urls = []
    if bsObj.find('td', attrs={'class', 'forum-t'}):
        object = bsObj.find_all('td', attrs={'class', 'forum-t'})
        for i in object:
            urls.append(i.a['href'])
    return urls

# 进入每一个url拿数据
def getCon(con):
    webBrowser.get(con)
    time.sleep(3)
    bsObjCon = BeautifulSoup(webBrowser.page_source, 'lxml')
    print bsObjCon.find('div', attrs={'class', 'content'}).get_text()

# 进入首页
if __name__ == '__main__':
    webBrowser = webdriver.PhantomJS()
    webBrowser.get('http://pp.163.com/pp/pub/')
    time.sleep(3)
    bsObj = BeautifulSoup(webBrowser.page_source, 'lxml')
    # 总的urls
    urls = []
    # 更新每一页的bsObj
    for i in xrange(1, 2):
        urls += getUrl(bsObj)
        webBrowser.find_element_by_xpath('//span[@class="pgi pgb pgbright iblock"]').click
        bsObj = BeautifulSoup(webBrowser.page_source, 'lxml')
    for i in urls:
        getCon(i)
    webBrowser.quit()
