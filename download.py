#coding:utf-8

import urllib,urllib2, re, lxml, urlparse, os, md5, time
from lxml import etree
from StringIO import StringIO
from HTMLParser import HTMLParser
import thread, threading, sys

from googletrans import Translator
from argparse import ArgumentParser
import html2text

import socket

translator = Translator()



html_parser = HTMLParser()

delta_d = 1
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
CODE = u'1j2l4n3k4n32m43n'
code_pat = re.compile(r'<code>.+?</code>')
def trans_so_from_url(url):
    T = get_dom_from_url(url)
    head = get_header(T)

    data = T.findall('//div[@class="post-text"]')

    out = []
    n = 0
  
    for d in data[:3]:
        xs = d.findall('./')
        ps = []
        ts = [] #fanyi
        cs = []
        for i, x in enumerate(xs):
            if x.tag in ('p', 'ul', 'ol'):
                html = dom_to_html(x)
                m = code_pat.findall(html)
                
                if m:
                    #print m 
                    html = code_pat.sub(CODE, html)
                    cs = cs + m
                ts.append((i, html_to_text(html)))
            else:
                ps.append((i, dom_to_html(x)))

        ids = [i for i,_ in ts]
        zh = translator.translate( [q for _, q in ts], src='en', dest='zh-CN')

        #print zh
        ps = sorted(ps + [(i, a.text) for i,a in zip(ids, zh)], key=lambda x:x[0])
        res = '\n'.join([q for _, q in ps])
        for code in cs:
            res = res.replace(CODE, code, 1)
        #print res
        out.append(res)
        n += 1
        if n == 1:
            out.append('[more]')

    body = html2text.html2text('\n'.join(out)).replace('[more]', '<!-- more -->\n\n')
    content = '\n\n'.join([head, body])
    return content.encode('utf-8')

from datetime import datetime, timedelta
def get_header(T):
    title = translator.translate(T.find('//div[@id="question-header"]/h1/a').text, src='en', dest='zh-CN').text
    tags = '\n\t'.join(['- ' + a.text for a in T.findall('//div[@class="post-taglist"]/a') if a.text is not None])
    d = T.find('//div[@id="question-header"]/h1/a').attrib['href'].split('/')[2]
    d = int(d) % 100
    dt = datetime(2018, 1, 14, 10, 0, 0) - timedelta(days=d)
    head = '''---
title: %s
date: %s
tags:
\t%s
---

''' % (
        title,
	dt.strftime('%Y-%m-%d %H:%M:%S'),
        tags
    )
    return head


#url = "https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do"

if __name__ == '__main__':
    paser = ArgumentParser()
    paser.add_argument("-f","--file", dest="file", default=False,  help="URL file")
    paser.add_argument("-o", "--output", dest="output", default='.',  help="output file name")
    paser.add_argument("-u", "--url", dest="url", default=False)
    args = paser.parse_args()

    if args.file:
        for url in open(args.file).read().split("\n"):
            if url.strip() == '':
                continue
            if url[-1] == '/':
                url = url[:-1]
            wfname = os.path.basename(url)
            fn = args.output + '/' + wfname + '.md'
            if os.path.exists(fn) and os.path.getsize(fn) > 0:
                continue
            fp = open(args.output + '/' + wfname + '.md', 'w')
            try:
                fp.write(trans_so_from_url(url))
            except Exception:
                print '[error]', url
            fp.close()

    elif args.url:
        url = args.url
        if args.output == '.':
            print trans_so_from_url(url)
        else:
            fp = open(args.output, 'w')
            fp.write(trans_so_from_url(url))
            fp.close()
