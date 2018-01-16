#coding:utf-8


import os
import re

def file_put_content(fn, data):
    fp = open(fn, 'w')
    fp.write(data)
    fp.close()

root = '/Users/zuoyuan/Documents/code/tracholar2.github.io/blog/source/_posts/'
fs = [root + f for f in os.listdir(root) if f not in ('.', '..')]

pat = re.compile(r'(^---.+?title:)(.+?)(\n.+?---)', re.M|re.S)

tags = {}
for f in  fs:
    data = open(f).read()
    m = pat.match(data)
    if m:
        print m.group(2)
        title = m.group(2).replace('.', ' ').replace("'", ' ').replace("<", '').replace('>', '').replace('\\','').replace('[重复]', '')
        file_put_content(f, pat.sub(m.group(1) + title + m.group(3), data))
        print f
