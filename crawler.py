# -*- coding:utf-8 -*-

from urllib.request import urlopen, quote
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re

def getResults(keyword):
    keywordBytes = bytes(keyword, 'gbk')
    url = 'http://s.dydytt.net/plus/search.php?kwtype=0&searchtype=title&keyword=%s' % quote(keywordBytes)
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        print('(HTTPError, URLError): ', e)
        return None
    try:
        bsObj = BeautifulSoup(html.read().decode('gb18030'), 'html.parser')
        contentDiv = bsObj.find('div', {'class': 'co_content8'})
        aTags = contentDiv.ul.findAll('a')
        return aTags
    except AttributeError as e:
        print('AttributeError: ', e)
        return None

def getDownloadList(name, url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        print('(HTTPError, URLError): ', e)
        return None
    try:
        bsObj = BeautifulSoup(html.read().decode('gb18030'), 'html.parser')
        tdTags = bsObj.findAll('td', {'bgcolor': "#fdfddf"})
        name = name.replace('/', '／')
        with open(name + '.txt', 'w') as f:
            for tdTag in tdTags:
                aTag = tdTag.a
                f.write(aTag.getText() + '\n')
        return True
    except AttributeError as e:
        print('AttributeError: ', e)
        return None

def main():
    keyword = input('TVs/Movies to search: ')
    aTags = getResults(keyword)
    if aTags == None:
        print('No results found')
    else:
        print('0 get all')
        for aTag in aTags:
            print(aTags.index(aTag) + 1, re.sub(r'<font color="red">|</font>', r'', aTag.getText()), ': http://www.ygdy8.com%s' % aTag['href'])
    choice = input('choose result(s) to get download links: ')
    choice = choice.split(' ')
    urlList = []
    if choice[0] == '0':
        urlList = aTags
    else:
        for i in choice:
            urlList.append(aTags[int(i) - 1])
    for urlInfo in urlList:
        result = getDownloadList(urlInfo.getText(), 'http://www.ygdy8.com' + urlInfo['href'])
        if result:
            print(urlInfo.getText(), 'success')
        else:
            print(urlInfo.getText(), 'failed')

if __name__ == '__main__':
    main()