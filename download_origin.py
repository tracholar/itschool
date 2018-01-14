#coding:utf-8

import urllib,urllib2, re, lxml, urlparse, os, md5, time
from lxml import etree
from StringIO import StringIO
from HTMLParser import HTMLParser
import thread, threading, sys

from googletrans import Translator
from argparse import ArgumentParser

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



def trans_so_from_url(url):
    T = get_dom_from_url(url)
    data = T.findall('//div[@class="post-text"]')

    out = []
    for d in data[:3]:
        #print res
        res = dom_to_html(d)
        out.append(res)
    return '\n'.join(out).encode('utf-8')


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
            fp = open(args.output + '/' + wfname + '.html', 'w')
            fp.write(trans_so_from_url(url))
            fp.close()

    elif args.url:
        url = args.url
        if args.output == '.':
            print trans_so_from_url(url)
        else:
            fp = open(args.output, 'w')
            fp.write(trans_so_from_url(url))
            fp.close()
