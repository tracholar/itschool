#coding:utf-8


from trans_html import *

urls = [
    ('http://news.qq.com/', '//div[@class="head"]')
]

visited_urls = set(open('.urls').read().split('\n'))

