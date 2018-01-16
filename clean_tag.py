#coding:utf-8
'''
只保留有限的tag
'''

import os
import re

def file_put_content(fn, data):
    fp = open(fn, 'w')
    fp.write(data)
    fp.close()

root = '/Users/zuoyuan/Documents/code/tracholar2.github.io/blog/source/_posts/'
fs = [root + f for f in os.listdir(root) if f not in ('.', '..')]

pat = re.compile(r'(^---.+?tags:\n)(.+?)(\n---)', re.M|re.S)

tags = {}
for f in  fs:
    data = open(f).read()
    m = pat.match(data)
    if m:
        for tg in m.group(2).strip().split('- '):
            tg = tg.strip()
            if tg!='':
                tags[tg] = tags.get(tg, 0) + 1

print sorted(tags.items(), key=lambda x: -x[1])[:50]


if True:
    tags = set(['html', 'python', 'javascript', 'java', 'c-sharp', 'php', 'bash', 'android', 'dot-net', 'css', 'shell', 'jquery', 'linux', 'unix', 'mysql', 'xml', 'html5','http',
                '区块链', '机器学习'])

    for f in  fs:
        data = open(f).read()
        m = pat.match(data)
        if m:
            print m.group(1),m.group(2),m.group(3)
            used_tags = [tg.strip() for tg in m.group(2).strip().split('- ') if tg.strip() in tags]
            file_put_content(f, pat.sub(m.group(1) + '\n'.join(['\t- ' + t for t in used_tags])+m.group(3), data))
            print '[FILE]', f
