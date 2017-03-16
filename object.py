# -*- coding:utf:8 -*-
class initSpider:
    def __init__(self):
        self.name='huhuibo'
        self.age='24'
    def getItem(self):
        uu=self.name+':from china'
        yy=int(self.age)+45
        print uu,'--',yy
if __name__ == '__main__':
    spider  = initSpider()
    spider.getItem()