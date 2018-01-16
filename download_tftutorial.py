#coding:utf-8

from trans_html import *
import html2text

url = 'https://www.tensorflow.org/tutorials/'
T = get_dom_from_url(url)
links = set([(a.attrib['href'], a.text) for a in T.findall('//ul[@class="devsite-nav-list"]/li/a')])
links = [(r,t) for r,t in links if r[:len(url)] == url]
print links

for r,t in links:
    print r
    title = translator.translate(t, src='en', dest='zh-CN').text


    T = get_dom_from_url(r)

    html = trans_html(T, '//div[@itemprop="articleBody"]')
    data = '#' + title + '\n\n' + html2text.html2text(html, r)

    fwname = os.path.basename(r) + '.md'
    file_put_content(fwname, data)





