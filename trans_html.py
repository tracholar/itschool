import urllib,urllib2, re, lxml, urlparse, os, time
from lxml import etree
from StringIO import StringIO
from HTMLParser import HTMLParser
import thread, threading, sys

from googletrans import Translator
from argparse import ArgumentParser
import html2text

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
    return etree.tostring(T, method='html')
def dom_to_text(T):
    return etree.tostring(T, method='text')
def html_to_text(html):
    return dom_to_text(get_dom_from_html(html))

CODE = 'CXJ743-HDK-53L'
code_pat = re.compile(r'<code>.+?</code>')

IMG = 'IMG32-4234jk3j4k3j4k'
img_pat = re.compile(r'<img.+?>', re.M|re.S|re.I|re.U)
def trans_html(T, xpath=None):
    if type(T) is str:
        T = get_dom_from_html(T)
    if type(T) is not etree._ElementTree:
        raise Exception("Not supporse!")

    if xpath is not None:
        T = T.find(xpath)
    
    xs = T.findall('./')
    ps = []
    ts = [] #fanyi
    cs = []
    imgs = []
    ts_tag_s = {}
    for i, x in enumerate(xs):
        if x.tag in ('p', 'ul', 'ol', 'blockquote', 'h1', 'h2', 'h3', 'h4', 'h5' , 'h6', 'aside'):
            html = dom_to_html(x)
            m = code_pat.findall(html)

            if m:
                #print m
                html = code_pat.sub(CODE, html)
                cs = cs + m

            m = img_pat.findall(html)
            if m:
                html = img_pat.sub(IMG, html)
                imgs = imgs + m
            ts.append((i, html_to_text(html)))
            ts_tag_s[i] = x.tag
        else:
            ps.append((i, dom_to_html(x)))

    ids = [i for i,_ in ts]
    zh = translator.translate( [q for _, q in ts], src='en', dest='zh-CN')

    #print zh
    ps = sorted(ps + [(i, '<' + ts_tag_s[i] + '>' + a.text + '</' + ts_tag_s[i] + '>') for i,a in zip(ids, zh)], key=lambda x:x[0])
    res = '\n'.join([q for _, q in ps])
    for code in cs:
        res = res.replace(CODE, code, 1)
    for im in imgs:
        res = res.replace(IMG, im, 1)

    return res






if __name__ == '__main__':
    html = get_dom_from_url(sys.argv[1])
    print trans_html(html, sys.argv[2])

