#coding:utf-8

import html2text
import sys


fn = sys.argv[1]
fp = open(fn.replace('.html', '.md'), 'w')
fp.write(html2text.html2text(open(sys.argv[1]).read().decode('utf-8')).encode('utf-8'))
fp.close()
