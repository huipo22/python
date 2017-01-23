# -*- coding:utf-8 -*-
import requests, re
from bs4 import BeautifulSoup

class InitSpider:
    # 初始化
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }

    #得到解析对象
    def get_bsObj(self, url):
        html = requests.get(url, self.headers).content
        soup = BeautifulSoup(html, 'lxml')
        return soup

    # 得到url列表
    def get_url(self, bsObj,reg):
        urlList = []
        urls=bsObj.find_all("a", href=re.compile(reg))
        for i in urls:
            if 'href' in i.attrs:
                urlList.append(i['href'])
        return urlList

    # 得到想要的内容
    def get_html(self,urlList,num):
        for i in urlList[:num]:
            bsObj=self.get_bsObj(i)
            data=dict()
            data['title']=bsObj.title
            print data


if __name__ == '__main__':
    # 入口
    spider = InitSpider()
    Init={
        'url':'http://news.baidu.com/',
        'reg':r'^h',
        'num':5
    }
    getObj = spider.get_bsObj(Init['url'])
    getUrl=spider.get_url(getObj,Init['reg'])
    spider.get_html(getUrl, Init['num'])