# -*- coding:utf-8 -*-
# author:huhuibo
# datetimes:2016-03-20


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from enSpiders.items import ArticleItem
from enSpiders.common import constant
from enSpiders.utils import datetimes

import datetime, re, requests
from enSpiders.clean.clean import content_dispose_image
from enSpiders.clean.baseclean import BaseClean
from bs4 import BeautifulSoup


class ArticleHealthSpider(CrawlSpider):
    """发现板块,health频道，themedicalfacts网站"""
    name = "themedicalfacts_health_explore"
    allowed_domains = ["themedicalfacts.com"]
    start_urls = [
        'http://www.themedicalfacts.com/category/medical-science/',
        'http://www.themedicalfacts.com/category/diet-food/home-remedies/',
        'http://www.themedicalfacts.com/category/diet-food/recipes/',
        'http://www.themedicalfacts.com/category/fitness-exercise/weight-gain/',
        'http://www.themedicalfacts.com/category/fitness-exercise/weight-loss/',
        'http://www.themedicalfacts.com/category/health/men/',
        'http://www.themedicalfacts.com/category/health/women/'
    ]
    rules = (Rule(LinkExtractor(allow=r"http://www.themedicalfacts.com/[\w].+"), callback="parse_item"),)

    # 翻页时用到的函数
    def getNextPage(self, nextUrl, requestUrl):
        # 存放图片
        pic = []
        # 存放body
        bodyDatas = []
        # 按顺序依次请求要访问的url
        for i in range(2, nextUrl + 1):
            rObj = requests.get(requestUrl + str(i))
            bsObj = BeautifulSoup(rObj.content, "lxml")
            figure = bsObj.find_all("figure", class_="wp-caption aligncenter")
            if figure:
                for i in figure:
                    tag = i.img
                    pic.append(tag["src"])
            bodyData = unicode(bsObj.find('div', 'td-post-content td-pb-padding-side'))
            bodyDatas.append(bodyData)
            # print bodyDatas
        # 最后返回回去
        return pic, bodyDatas

    def parse_item(self, response):
        # 使用bs 删除标签，替换标签
        bsObj = BeautifulSoup(response.body, "lxml")
        if bsObj.script:
            [s.extract() for s in bsObj.find_all("script")]
        # 配置
        conf = {
            'lastTime': 360,
            'pageTime': response.xpath('//meta[@property="article:published_time"]/@content').extract(),
            'Title': ''.join(response.xpath('//meta[@name="twitter:title"]/@content').extract()).strip(),
            'userName': '',
            'channelId': constant.C_ID_ALL,
            'img_s': response.xpath('//figure[@class="wp-caption aligncenter"]/img/@src').extract(),
            'front_three_data': response.xpath('//div[@class="td-post-content td-pb-padding-side"]//p'),
            'Channel': constant.IS_ORIGINAL_TWO,
            'source': 'themedicalfacts',
            'body': unicode(bsObj.find("div", attrs={"class", "td-post-content td-pb-padding-side"}))
        }
        now = datetime.datetime.now()
        ninth = datetime.timedelta(days=conf['lastTime'])
        # 过去三个月
        last = now - ninth

        if not conf['pageTime']:
            return None

        pageTime = conf['pageTime'][0][:10]
        # 网页上的时间
        webTime = datetime.datetime.strptime(pageTime, '%Y-%m-%d')

        # 网页上的时间
        # print 'nowTime:', conf['pageTime']
        if webTime > last:
            requestUrl = response.url
            # 初始化 pic  bodyDatas  用来接 函数的返回值
            pic = []
            bodyDatas = []
            if response.xpath('//i[@class="td-icon-menu-right"]'):
                # 查看有多少页
                nextUrl = int(
                    response.xpath('//div[@class="page-nav page-nav-post td-pb-padding-side"]/a/@href').extract()[-2][
                        -2])
                # 调用翻页函数
                pic, bodyDatas = self.getNextPage(nextUrl, requestUrl)

            item = ArticleItem()
            item['title'] = conf['Title']
            item['create_date'] = datetimes.get_current_datetime()
            item['channel_id'] = conf['channelId']
            imgUrl = []
            Imgs = conf['img_s'] + pic
            if Imgs:
                imgUrl += Imgs

            imgUrls = []
            if imgUrl:
                for i in imgUrl:
                    i = ''.join(i)
                    i = i.split('?')
                    imgUrls.append(i[0])
            else:
                imgUrls = []

            item['original_files'] = imgUrls

            item['template'] = ''
            data = conf['front_three_data']
            info = data.xpath('string(.)').extract()
            content = []
            for i in range(len(info)):
                if info[i] != '\n':
                    content.append(info[i].strip())
            item['content'] = content[0:3]
            item['is_original'] = conf['Channel']
            item['source'] = conf['source']
            item['user_id'] = constant.USER_ID
            item['user_name'] = conf['userName']
            item['user_avatar'] = ''
            item['status'] = constant.STATUS_TWO
            item['comment_num'] = 0
            item['agree_num'] = 0
            item['page_url'] = response.url
            item['update_date'] = datetimes.get_current_datetime()
            item['language'] = constant.LANGUAGE_ONE
            item['category'] = constant.CATEGORY_ONE

            # 网站描述
            description = response.xpath("//meta[@name='description']/@content")
            if description:
                item['tag'] = description.extract()[0]
            else:
                item['tag'] = ''

            body = [conf['body']] + bodyDatas
            bclean = BaseClean()
            img_re = []
            for i in imgUrls:
                img_re.append(i.replace('?', '\?'))

            item["body"] = bclean.format_content(content_dispose_image(body, img_re), 'p')

            item['body_files'] = ""
            item['cover'] = ""
            item['mysqlID'] = ""
            item['country'] = constant.COUNTRY

            img_num = re.compile(r'<p>IMG_[0-9]{1,}</p>')
            num = re.findall(img_num, item['body'])

            if item['body']:
                if len(num) == len(item['original_files']):
                    # print item
                    return item
            else:
                return
