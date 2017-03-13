from selenium import webdriver
import time
webBrowser = webdriver.Chrome()
print 'run ...'
webBrowser.get('https://scienceblog.com/492785/castration-resistant-prostate-cancer-cell-growth-impeded-endostatin/')
print 'get start ...'
con=webBrowser.find_elements_by_xpath('//div[@class="entry-content"]//p')
for i in con:
    print i.text
print 'get over ........'
