#coding:utf-8

import urllib,urllib2, re, lxml, urlparse, os, md5, time
from lxml import etree
from StringIO import StringIO
from HTMLParser import HTMLParser
import thread, threading, sys

from googletrans import Translator
translator = Translator()



html_parser = HTMLParser()

def html_parse(html):
    return html_parser.unescape(html)


def get_data_from_url(url):

    print '[visit]', url
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36',
    }
    req = urllib2.Request(url, headers = headers)
    try:
        data = urllib2.urlopen(req).read()
    except Exception:
        data = ''
    return data

def get_dom_from_html(html):
    return etree.parse(StringIO(html), etree.HTMLParser())

def get_dom_from_url(url):
    html = get_data_from_url(url)
    html = html.replace('<ol>', '<ul>').replace('</ol>', '</ul>').replace('<sub>', '').replace('</sub>', '')
    T = get_dom_from_html(html)
    return T

def dom_to_html(T):
    return etree.tostring(T, pretty_print=True)


url = "https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do"


T = get_dom_from_url(url)
data = T.findall('//div[@class="post-text"]')

out = []
for d in data[:3]:
    xs = d.findall('./')
    ps = []
    ts = [] #fanyi
    for i, x in enumerate(xs):
        if x.tag in ('p', 'ul', 'ol'):
            ts.append((i, dom_to_html(x)))
        else:
            ps.append((i, dom_to_html(x)))

    ids = [i for i,_ in ts]
    zh = translator.translate( [q for _, q in ts], src='en', dest='zh-CN')

    #print zh
    ps = sorted(ps + [(i, a.text) for i,a in zip(ids, zh)], key=lambda x:x[0])
    res = '\n'.join([q for _, q in ps]).replace('</ ', '</')
    print res
    out.append(res)

fp = open('out.html', 'w')
fp.write('\n'.join(out).encode('utf-8'))
