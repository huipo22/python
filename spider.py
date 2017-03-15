from selenium import webdriver
import time
from bs4 import BeautifulSoup
webBrowser = webdriver.Chrome()
print 'run ...'
webBrowser.get('http://pp.163.com/pp/pub/')
time.sleep(10)
bsObj=BeautifulSoup(webBrowser.page_source,'lxml')
print 'get start ...'
print bsObj.find_all('td')
print '----------------------'
for i in bsObj.find_all('td'):
    print i.get_text()
    
print 'get over ........'
webBrowser.quit()