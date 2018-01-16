#coding:utf-8


import os
import re

def file_put_content(fn, data):
    fp = open(fn, 'w')
    fp.write(data)
    fp.close()

root = '/Users/zuoyuan/Documents/code/tracholar2.github.io/blog/source/_posts/'
fs = [root + f for f in os.listdir(root) if f not in ('.', '..')]

pat = re.compile(r'^---.+?- (\.net).+?---', re.M|re.S)
for f in  fs:
    data = open(f).read()
    m = pat.match(data)
    if m:
        print m.group()
        new_head = m.group().replace('.net', 'dot-net')
        new_data = pat.sub(new_head, data)
        file_put_content(f, new_data)
        print '[FILE]', f