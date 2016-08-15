# -*- coding:utf-8 -*-

import os
import re
from urllib.request import urlopen, quote
from urllib.error import HTTPError, URLError
from datetime import date

from bs4 import BeautifulSoup

use_db = True

try:
    from pymongo import MongoClient
    print('pymongo found, running on db mode!')
except ImportError as e:
    use_db = False
    print('import error:', e)
    print('running on no db mode!')

def get_results(keyword):
    keyword_bytes = bytes(keyword, 'gbk')
    url = 'http://s.dydytt.net/plus/search.php?kwtype=0&searchtype=title&keyword=%s' % quote(keyword_bytes)
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        print('(HTTPError, URLError): ', e)
        return None
    try:
        bs_obj = BeautifulSoup(html.read().decode('gb18030'), 'html.parser')
        content_div = bs_obj.find('div', {'class': 'co_content8'})
        a_tags = content_div.ul.findAll('a')
        return a_tags
    except AttributeError as e:
        print('AttributeError: ', e)
        return None

def get_download_list(name, url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        print('(HTTPError, URLError): ', e)
        return None
    try:
        bs_obj = BeautifulSoup(html.read().decode('gb18030'), 'html.parser')
        td_tags = bs_obj.findAll('td', {'bgcolor': "#fdfddf"})
        name = name.replace('/', '／')
        file_path = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = os.path.join(file_path, name)
        with open(file_name + '.txt', 'w') as f:
            f.write(str(date.today()) + '\n')
            for td_tag in td_tags:
                a_tag = td_tag.a
                f.write(a_tag.getText() + '\n')
        return True
    except AttributeError as e:
        print('AttributeError: ', e)
        return None

def main():
    keyword = input('TVs/Movies to search: ')
    a_tags = get_results(keyword)
    if a_tags == None:
        print('No results found')
    else:
        print('0 | get all')
        for a_tag in a_tags:
            print(a_tags.index(a_tag) + 1, '|', re.sub(r'<font color="red">|</font>', r'', a_tag.getText()), ': http://www.ygdy8.com%s' % a_tag['href'])
    print(len(a_tags) + 1, '| exit')
    choice = input('choose result(s) to get download links: ')
    choice = choice.split(' ')
    url_list = []
    if choice[0] == '0':
        url_list = a_tags
    elif str(len(a_tags) + 1) in choice:
        return
    else:
        for i in choice:
            url_list.append(a_tags[int(i) - 1])
    for url_info in url_list:
        result = get_download_list(url_info.getText(), 'http://www.ygdy8.com' + url_info['href'])
        if result:
            print('require', url_info.getText(), 'success')
        else:
            print('require', url_info.getText(), 'failed')

if __name__ == '__main__':
    main()
