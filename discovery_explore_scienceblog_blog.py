# -*- coding:utf-8 -*-
# author:huhuibo
# datetimes:2016-03-14


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from enSpiders.items import ArticleItem
from enSpiders.common import constant
from enSpiders.utils import datetimes

import datetime, re
from enSpiders.clean.clean import content_dispose_image
from enSpiders.clean.baseclean import BaseClean
from bs4 import BeautifulSoup


class ArticleHealthSpider(CrawlSpider):
    """发现板块,科学频道，science20网站"""
    name = "scienceblog_blog_explore"
    allowed_domains = ["scienceblog.com"]
    start_urls = \
        ['https://scienceblog.com/category/brain-behave/page/{}'.format(x) for x in range(1, 370)] + [
            'https://scienceblog.com/category/earth-energy-environment/page/{}'.format(x) for x in range(1, 1550)] + [
            'https://scienceblog.com/category/lifenonhumans/page/{}'.format(x) for x in range(1, 1100)] + [
            'https://scienceblog.com/category/physics-math/page/{}'.format(x) for x in range(1, 520)] + [
            'https://scienceblog.com/category/space-planets/page/{}'.format(x) for x in range(1, 520)] + [
            'https://scienceblog.com/category/techengineering/page/{}'.format(x) for x in range(1, 330)]
    rules = (Rule(LinkExtractor(allow=r"https://scienceblog.com/[\d_].+/[\w_].+"), callback="parse_item"),)

    def parse_item(self, response):
        # 使用bs 删除标签，替换标签
        bsObj = BeautifulSoup(response.body, "lxml")
        if bsObj.script:
            [s.extract() for s in bsObj.find_all("script")]
        if bsObj.footer:
            [s.extract() for s in bsObj.find_all("footer")]

        # 配置
        conf = {
            'lastTime': 93,
            'pageTime': response.xpath('//meta[@property="article:published_time"]/@content').extract()[0][:10],
            'Title': ''.join(response.xpath('//h1[@class="entry-title"]/text()').extract()).strip(),
            'userName': '',
            'channelId': constant.C_ID_BLOGS,
            'img_s': response.xpath('//img[@class="attachment-full size-full"]/@src').extract(),
            'front_three_data': response.xpath('//div[@class="entry-content"]//p'),
            'Channel': constant.IS_ORIGINAL_TWO,
            'source': 'ScienceBlog',
            'body': str(bsObj.find("div", attrs={"class", "inside-article"}))
        }

        now = datetime.datetime.now()
        ninth = datetime.timedelta(days=conf['lastTime'])
        # 过去三个月
        last = now - ninth
        pageTime = conf['pageTime']
        # 网页上的时间
        webTime = datetime.datetime.strptime(pageTime, '%Y-%m-%d')
        print 'nowTime:', webTime
        if webTime > last:
            item = ArticleItem()
            item['title'] = conf['Title']
            item['create_date'] = datetimes.get_current_datetime()
            item['channel_id'] = conf['channelId']
            imgUrl = []
            Imgs = conf['img_s']
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

            body = conf['body']
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
                    print item
                    return item
            else:
                return
