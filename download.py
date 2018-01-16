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
from trans_html import *


def trans_so_from_url(url):
    T = get_dom_from_url(url)
    head = get_header(T)

    data = T.findall('//div[@class="post-text"]')

    out = []
    n = 0
  
    for d in data[:3]:
        res = trans_html(d)

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
