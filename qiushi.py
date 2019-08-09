#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import os
import re
import time
import ssl

RESULT_DIR = 'Result'
HOST = 'https://www.qiushibaike.com'
MAX_REQUEST_PAGE_NUM = 26

def initDir():
    if not os.path.isdir(RESULT_DIR):
        os.makedirs(RESULT_DIR)
    return

def getHtml(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    request = urllib2.Request(url, headers = headers)
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.code
        print e.reason
        return None
    else:
        html = response.read()
        return html

def getNextPageUrl(currentPage):
    pattern = re.compile(u'<li>.*?<span class=".*?">.*?13.*?<li>.*?<a href="(.*?)" rel="nofollow">.*<span class="next">', re.S)
    result = re.findall(pattern, currentPage)
    if result:
        return result[len(result) - 1]
    return None


def save(data, fileName):
    fp = open(fileName, 'w')
    if isinstance(data, str):
        fp.write(data)
    if isinstance(data, list):
        fp.writelines(data)
    fp.close()
    return

def load(path):
    url = HOST + path
    html = getHtml(url)
    return html

def hanleBr(string):
    return string.replace('<br/>', '\r\n')

def prase(html):
    pattern = re.compile(u'<div class="author clearfix">.*?<h2>(.*?)</h2>.*?</div>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>', re.S)
    result = re.findall(pattern, html)
    formatResults = []
    if len(result) > 0:
        for item in result:
            idx = 0
            if isinstance(item, tuple):
                string=""
                for string in item:
                    if string == item[len(item)-1]:
                        string = hanleBr(string) + '/--------------------------------------------------/' + '\n\r'
                    formatResults.append(string)
            if isinstance(item, str):
                formatResults.append(hanleBr(item) + '\n\r')
    return formatResults 

def fileIsExists(page):
    resultPath = '%s/page%d.txt' % (RESULT_DIR, page)
    if os.path.exists(resultPath):
        return True
    return False



initDir()
page = 1
while 1:
    if fileIsExists(page):
        page = page + 1
        continue
    break
path = "/hot"
originPage = page
ssl._create_default_https_context = ssl._create_unverified_context
while 1:
    htmlData = load(path)
    if not htmlData == None:
        results = prase(htmlData)
        if len(results) > 0:
            resultPath = '%s/page%d.txt' % (RESULT_DIR, page)
            save(results, resultPath)
            nextPath = getNextPageUrl(htmlData)
            if not nextPath == None:
                path = nextPath
                page = page + 1
                if page == originPage + MAX_REQUEST_PAGE_NUM:
                    break
                continue
        break
print 'Misson Complete!'
    
