# -*- coding:utf-8 -*-
import requests, re
from bs4 import BeautifulSoup

# headers
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
# 先从首页爬取 ---- 新闻的a链接
url = 'http://news.baidu.com/'
# 用 bs4 获取首页内容
html = requests.get(url).content
# 用'lxml'解析首页
soup = BeautifulSoup(html, 'lxml')

urlList = []
# 获取所有的a链接中的href 放入url_list
url_list = soup.find_all('a', href=re.compile(r'^h'))
# 循环取 a链接 ---- 放入urlList
for i in url_list:
    if 'href' in i.attrs:
        urlList.append(i['href'])
# 开始循环爬网站
for j in urlList:  
    html = requests.get(j).content
    index_data = BeautifulSoup(html, 'lxml')
    data = dict()
    data['title'] = index_data.title
    print data
