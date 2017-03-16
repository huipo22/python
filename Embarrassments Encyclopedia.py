# -*- coding:utf:8 -*-

# 糗事百科

'''
    网页返回503 那就让时间隔10去爬取
'''
import requests
import time
from bs4 import BeautifulSoup


class initSpider:
    def __init__(self):
        self.pageIndex = 0
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }

    def main(self, url):

        # urls存放所有url链接
        urls=[]
        for i in range(20):
            self.pageIndex += 1
            urls.append(self.pageIndex)

        #  依次爬取urls中的url链接
        for j in urls:
            time.sleep(3)
            print u'第', j, u'页：'
            pageCon = requests.get(url + str(j), self.headers).content
            soup = BeautifulSoup(pageCon, 'lxml')
            oDiv = soup.find_all('div', 'content')
            for i in oDiv:
                if i.span:
                    # pass
                    print i.span.text
                else:
                    'not find'


if __name__ == '__main__':
    spider = initSpider()
    url = 'http://www.qiushibaike.com/8hr/page/'
    spider.main(url)
